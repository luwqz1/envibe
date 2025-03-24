import inspect
import os
import pathlib
import re
import shlex
import types
from collections import OrderedDict
from collections.abc import Mapping
from typing import Final

from felis import either, identity, option

from envibe.tools import function_to_lazy, optional_to_option

ASSIGNMENT_OPERATOR: Final[str] = "="
VARIABLE_NAME_PATTERN: Final[re.Pattern[str]] = re.compile(r"[A-Za-z_][A-Za-z_0-9]*")


take = function_to_lazy(os.environ.__getitem__)


safe_take = function_to_lazy(either.catch(KeyError)(os.environ.__getitem__))


take_option = function_to_lazy(identity.compose(optional_to_option)(os.environ.get))


def _tokens_to_value(tokens: list[str], /) -> str:
    return "".join(tokens).replace(r"\n", "\n").replace(r"\t", "\t")


def get_caller_directory() -> option.Option[pathlib.Path]:
    current_frame = inspect.currentframe()
    if current_frame is None:
        return None

    frame = current_frame
    while True:
        match frame.f_back:
            case types.FrameType() as f:
                frame = f
            case _:
                break

    path = pathlib.Path(frame.f_code.co_filename).resolve().parent
    return option.Some(path)


def find_env_file(start_path: pathlib.Path, /) -> option.Option[pathlib.Path]:
    """Search for a `.env` file starting from the given path.

    The function first searches recursively through all subdirectories
    of the provided start_path. If no .env file is found, it then searches
    upwards through each parent directory until the root.

    :param start_path: The starting directory path from which the search begins.
    """

    for path in start_path.rglob(".env"):
        return option.Some(path)

    for parent in start_path.parents:
        env_path = parent / ".env"
        if env_path.exists():
            return option.Some(env_path)

    return None


def parse_dotenv(content: str, /) -> Mapping[str, str]:
    """Parse a `.env` file content as an ordered mapping."""
    variables = OrderedDict[str, str]()

    for line in content.splitlines():
        match tuple(shlex.shlex(instream=line, posix=True)):
            case (var, operator, *tokens) if operator == ASSIGNMENT_OPERATOR \
                and VARIABLE_NAME_PATTERN.match(var):
                variables[var] = _tokens_to_value(tokens)
            case _:
                continue

    return variables


__all__ = (
    "parse_dotenv",
    "find_env_file",
    "get_caller_directory",
    "safe_take",
    "take",
    "take_option",
)
