from enum import Enum

from public import public


@public
class VisibilityKind(Enum):
    public: int = 1
    private: int = 2


@public
class ScopeKind(Enum):
    global_: int = 1
    local: int = 2
