import os
import pathlib

from felis import option

from envibe.error import ResolvePathError
from envibe.parser import find_env_file, get_caller_directory, parse_dotenv, safe_take, take, take_option
from envibe.tools import option_to_optional, optional_to_option


def read_dotenv(path: str | pathlib.Path | None = None, /, *, override: bool = False) -> None:
    """Read a `.env` and set variables into the `os._Environ` object."""
    
    path = option_to_optional(get_caller_directory()) \
        if path is None \
        else option_to_optional(option.map(pathlib.Path)(optional_to_option(path)))

    if path is None:
        raise ResolvePathError(
            "Cannot to resolve the path by the caller frame. "
            "Ensure that the caller frame is not a built-in function or module. "
            "Consider passing the path explicitly as an argument."
        )

    match find_env_file(path):
        case option.Some(env_file):
            setter = os.environ.__setitem__ if override else os.environ.setdefault
            for var, val in parse_dotenv(env_file.read_text(encoding="UTF-8")).items():
                setter(var, val)
        case _:
            raise FileNotFoundError(
                f"No .env file found starting from {str(path)!r} — "
                "searched recursively in all subdirectories and upwards through parent directories. "
                "Ensure that the .env file exists somewhere along the directory structure relative "
                "to the starting path."
            )


__all__ = (
    "ResolvePathError",
    "find_env_file",
    "get_caller_directory",
    "read_dotenv",
    "safe_take",
    "take",
    "take_option",
)
