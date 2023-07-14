from arxast.base import DataType, ASTKind, SourceLocation, Expr, ExprType


class Number(DataType):
    """Number data type expression."""


class Integer(Number):
    """Integer number data type expression."""

    value: int

    def __init__(self, value: int):
        self.value = value

    @classmethod
    @property
    def name(cls) -> str:
        return cls.__name__.lower()


class SignedInteger(Integer):
    """Signed integer number data type expression."""


class Int8(SignedInteger):
    """Int8 data type expression."""


class Int16(SignedInteger):
    """Int16 data type expression."""


class Int32(SignedInteger):
    """Int32 data type expression."""


class Int64(SignedInteger):
    """Int64 data type expression."""


class Floating(Number):
    """AST for the literal float number."""

    value: float

    def __init__(
        self, val: float, loc: SourceLocation = SourceLocation(0, 0)
    ) -> None:
        """Initialize the FloatAST instance."""
        self.loc = loc
        self.value = val
        self.kind = ASTKind.FloatDTKind


class Float16(Floating):
    """Float16 data type expression."""


class Float32(Floating):
    """Float32 data type expression."""


class Float64(Floating):
    """Float64 data type expression."""

class Boolean(DataType):
    """Boolean data type expression."""

    value: bool

    def __init__(self, value: bool):
        self.value = value

class Variable(Expr):
    """AST class for the variable usage."""

    type_: ExprType

    def __init__(self, name: str, type_: ExprType, loc: SourceLocation) -> None:
        """Initialize the Variable instance."""
        super().__init__(loc)
        self.name = name
        self.type_ = type_
        self.kind = ASTKind.VariableKind
