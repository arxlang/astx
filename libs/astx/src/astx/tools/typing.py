"""Tools for typing support helper."""

from typing import Any, Callable, TypeVar

from public import public
from typeguard import (
    CollectionCheckStrategy,
    ForwardRefPolicy,
)
from typeguard import (
    typechecked as _typechecked,
)
from typeguard._config import global_config

_T = TypeVar("_T")


__all__ = ["typechecked"]


@public
def skip_unused(*args: Any, **kwargs: Any) -> None:
    """Referencing variables to pacify static analyzers."""
    for arg in args:
        pass
    for key in kwargs:
        pass


@public
def copy_type(f: _T) -> Callable[[Any], _T]:
    """Copy types for args, kwargs from parent class."""
    skip_unused(f)
    return lambda x: x


typechecked = _typechecked(
    forward_ref_policy=ForwardRefPolicy.IGNORE,
    collection_check_strategy=CollectionCheckStrategy.ALL_ITEMS,
)

# Override the default configuration
global_config.forward_ref_policy = ForwardRefPolicy.IGNORE
global_config.collection_check_strategy = CollectionCheckStrategy.ALL_ITEMS
