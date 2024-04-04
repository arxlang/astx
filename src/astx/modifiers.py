"""Modifications for ASTx, such as visibility, scope, etc."""

from enum import Enum

from public import public


@public
class VisibilityKind(Enum):
    """Definition of different kind of visibility."""

    public: int = 1
    private: int = 2
    protected: int = 3


@public
class ScopeKind(Enum):
    """Definition for different kind of scopes."""

    global_: int = 1
    local: int = 2


@public
class MutabilityKind(Enum):
    """Definition for different kind of mutability."""

    constant: int = 1
    mutable: int = 2
