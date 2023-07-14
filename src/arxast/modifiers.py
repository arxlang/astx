from enum import Enum


class VisibilityKind(Enum):
    public: int = 1
    private: int = 2


class ScopeKind(Enum):
    global_: int = 1
    local: int = 2
