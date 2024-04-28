"""Tools for typing support helper."""

from typing import Any, Callable, TypeVar

_T = TypeVar("_T")


def skip_unused(*args: Any, **kwargs: Any) -> None:
    """Referencing variables to pacify static analyzers."""
    for arg in args:
        pass
    for key in kwargs:
        pass


def copy_type(f: _T) -> Callable[[Any], _T]:
    """Copy types for args, kwargs from parent class."""
    skip_unused(f)
    return lambda x: x
