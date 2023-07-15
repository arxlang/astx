from astx.base import DataType, ASTKind, SourceLocation, Expr, ExprType


class Number(DataType):
    """Number data type expression."""


class Integer(Number):
    """Integer number data type expression."""


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


class Float16(Floating):
    """Float16 data type expression."""


class Float32(Floating):
    """Float32 data type expression."""


class Float64(Floating):
    """Float64 data type expression."""


class Boolean(DataType):
    """Boolean data type expression."""


class Literal(DataType):
    """Literal Data type."""

    type_: ExprType
    loc: SourceLocation


class Int32Literal(Literal):
    value: int

    def __init__(
        self, value: int, loc: SourceLocation = SourceLocation(0, 0)
    ) -> None:
        self.value = value
        self.type_ = Int32
        self.loc = loc


class Variable(Expr):
    """AST class for the variable usage."""

    type_: ExprType

    def __init__(
        self,
        name: str,
        type_: ExprType,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the Variable instance."""
        super().__init__(loc)
        self.name = name
        self.type_ = type_
        self.kind = ASTKind.VariableKind
