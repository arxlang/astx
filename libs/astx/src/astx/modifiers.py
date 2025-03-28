"""Modifications for ASTx, such as visibility, scope, etc."""

from enum import Enum

from public import public


@public
class VisibilityKind(Enum):
    """Definition of different kind of visibility."""

    public = 1
    private = 2
    protected = 3


@public
class ScopeKind(Enum):
    """Definition for different kind of scopes."""

    global_ = 1
    local = 2


@public
class MutabilityKind(Enum):
    """Definition for different kind of mutability."""

    constant = 1
    mutable = 2
