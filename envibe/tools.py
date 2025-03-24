from collections.abc import Callable
from typing import Any

from felis import currying, either, lazy, option


def either_to_option[L](e: either.Either[Any, L], /) -> option.Option[L]:
    match e:
        case either.Left(_):
            return None
        case either.Right(value):
            return option.Some(value)


@currying.curry
def option_to_either[L, R](opt: option.Option[R], default: L, /) -> either.Either[L, R]:
    match opt:
        case option.Some(value):
            return either.Right(value)
        case None:
            return either.Left(default)


def optional_to_option[T](value: T | None, /) -> option.Option[T]:
    return option.Some(value) if value is not None else None


def option_to_optional[T](opt: option.Option[T], /) -> T | None:
    match opt:
        case option.Some(value):
            return value
        case None:
            return None


def function_to_lazy[**P, R](f: Callable[P, R], /) -> Callable[P, lazy.Lazy[R]]:
    return lambda *args, **kwargs: lambda: f(*args, **kwargs)


__all__ = (
    "function_to_lazy",
    "either_to_option",
    "option_to_either",
    "optional_to_option",
    "option_to_optional",
)
