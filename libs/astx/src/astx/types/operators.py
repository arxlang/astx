"""ASTx Data Types module."""

from __future__ import annotations

from typing import Optional

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    DataType,
    ExprType,
    ReprStruct,
    SourceLocation,
)
from astx.tools.typing import typechecked


@public
@typechecked
class DataTypeOps(DataType):
    """Overload some magic functions used for the main operations."""

    def __hash__(self) -> int:
        """Ensure that the hash method is not None."""
        return super().__hash__()

    def __add__(self, other: DataType) -> BinaryOp:
        """Overload the magic `add` method."""
        return BinaryOp("+", self, other)

    def __eq__(self, other: DataType) -> BinaryOp:  # type: ignore
        """Overload the magic `eq` method."""
        return BinaryOp("==", self, other)

    def __floordiv__(self, other: DataType) -> BinaryOp:
        """Overload the magic `floordiv` method."""
        return BinaryOp("//", self, other)

    def __ge__(self, other: DataType) -> BinaryOp:
        """Overload the magic `ge` method."""
        return BinaryOp(">=", self, other)

    def __gt__(self, other: DataType) -> BinaryOp:
        """Overload the magic `gt` method."""
        return BinaryOp(">", self, other)

    def __le__(self, other: DataType) -> BinaryOp:
        """Overload the magic `le` method."""
        return BinaryOp("<=", self, other)

    def __lt__(self, other: DataType) -> BinaryOp:
        """Overload the magic `lt` method."""
        return BinaryOp("<", self, other)

    def __mod__(self, other: DataType) -> BinaryOp:
        """Overload the magic `mod` method."""
        return BinaryOp("%", self, other)

    def __mul__(self, other: DataType) -> BinaryOp:
        """Overload the magic `mul` method."""
        return BinaryOp("*", self, other)

    def __ne__(self, other: DataType) -> BinaryOp:  # type: ignore
        """Overload the magic `ne` method."""
        return BinaryOp("!=", self, other)

    def __neg__(self) -> UnaryOp:
        """Overload the magic `neg` method."""
        return UnaryOp("-", self)

    def __pos__(self) -> UnaryOp:
        """Overload the magic `pos` method."""
        return UnaryOp("+", self)

    def __pow__(self, other: DataType) -> BinaryOp:
        """Overload the magic `pow` method."""
        return BinaryOp("^", self, other)

    def __sub__(self, other: DataType) -> BinaryOp:
        """Overload the magic `sub` method."""
        return BinaryOp("-", self, other)

    def __truediv__(self, other: DataType) -> BinaryOp:
        """Overload the magic `truediv` method."""
        return BinaryOp("/", self, other)

    def __and__(self, other: DataType) -> AndOp:
        """Overload the magic 'and' method."""
        return AndOp(self, other)

    def __or__(self, other: DataType) -> OrOp:
        """Overload the magic 'or' method."""
        return OrOp(self, other)

    def __xor__(self, other: DataType) -> XorOp:
        """Overload the magic 'xor' method."""
        return XorOp(self, other)

    def __invert__(self) -> NotOp:
        """Overload the magic 'not' method."""
        return NotOp(self)


@public
@typechecked
class UnaryOp(DataTypeOps):
    """AST class for the unary operator."""

    op_code: str
    operand: DataType

    def __init__(
        self,
        op_code: str,
        operand: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the UnaryOp instance."""
        super().__init__(loc=loc, parent=parent)
        self.op_code = op_code
        self.operand = operand
        self.kind = ASTKind.UnaryOpKind

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"UnaryOp[{self.op_code}]({self.operand})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = f"UNARY[{self.op_code}]"
        value = self.operand.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class BinaryOp(DataTypeOps):
    """AST class for the binary operator."""

    type_: ExprType
    lhs: DataType
    rhs: DataType
    op_code: str

    def __init__(
        self,
        op_code: str,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the BinaryOp instance."""
        super().__init__(loc=loc, parent=parent)

        self.op_code = op_code
        self.lhs = lhs
        self.rhs = rhs
        self.kind = ASTKind.BinaryOpKind

        if not (
            isinstance(lhs.type_, DataType) and isinstance(rhs.type_, DataType)
        ):
            raise Exception(
                "For now, binary operators are just allowed for `DataType`."
                f"LHS: {lhs.type_}, RHS: {rhs.type_}"
            )

        if lhs.type_ == rhs.type_:
            self.type_ = lhs.type_
        else:
            # type inference
            self.type_ = max([lhs.type_, rhs.type_], key=lambda v: v.nbytes)

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"BinaryOp[{self.op_code}]({self.lhs},{self.rhs})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure that represents the object."""
        key = f"BINARY[{self.op_code}]"
        lhs = {"lhs": self.lhs.get_struct(simplified)}
        rhs = {"rhs": self.rhs.get_struct(simplified)}

        content: ReprStruct = {**lhs, **rhs}
        return self._prepare_struct(key, content, simplified)


@public
@typechecked
class BoolBinaryOp(BinaryOp):
    """Base AST class for boolean binary operations."""

    def __init__(
        self,
        op_code: str,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(
            op_code=op_code,
            lhs=lhs,
            rhs=rhs,
            loc=loc,
            parent=parent,
        )

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"({self.lhs} {self.op_code} {self.rhs})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure that represents the object."""
        key = f"BOOL_BINARY_OP[{self.__class__.__name__}]"
        value: ReprStruct = {
            "lhs": self.lhs.get_struct(simplified),
            "rhs": self.rhs.get_struct(simplified),
        }
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class BoolUnaryOp(UnaryOp):
    """Base AST class for boolean unary operations."""

    def __init__(
        self,
        op_code: str,
        operand: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(
            op_code=op_code,
            operand=operand,
            loc=loc,
            parent=parent,
        )

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"({self.op_code} {self.operand})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure that represents the object."""
        key = f"BOOL_UNARY_OP[{self.__class__.__name__}]"
        value: ReprStruct = {"operand": self.operand.get_struct(simplified)}
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class AndOp(BoolBinaryOp):
    """AST class for logical AND operation."""

    kind = ASTKind.AndOpKind
    op_code = "and"

    def __init__(
        self,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Instantiate AST class for logical AND operation."""
        super().__init__(
            op_code=self.op_code,
            lhs=lhs,
            rhs=rhs,
            loc=loc,
            parent=parent,
        )


@public
@typechecked
class OrOp(BoolBinaryOp):
    """AST class for logical OR operation."""

    kind = ASTKind.OrOpKind
    op_code = "or"

    def __init__(
        self,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Instantiate AST class for logical OR operation."""
        super().__init__(
            op_code=self.op_code,
            lhs=lhs,
            rhs=rhs,
            loc=loc,
            parent=parent,
        )


@public
@typechecked
class XorOp(BoolBinaryOp):
    """AST class for logical XOR operation."""

    kind = ASTKind.XorOpKind
    op_code = "xor"

    def __init__(
        self,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Instantiate AST class for logical XOR operation."""
        super().__init__(
            op_code=self.op_code,
            lhs=lhs,
            rhs=rhs,
            loc=loc,
            parent=parent,
        )


@public
@typechecked
class NandOp(BoolBinaryOp):
    """AST class for logical NAND operation."""

    kind = ASTKind.NandOpKind
    op_code = "nand"

    def __init__(
        self,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Instantiate AST class for logical NAND operation."""
        super().__init__(
            op_code=self.op_code,
            lhs=lhs,
            rhs=rhs,
            loc=loc,
            parent=parent,
        )


@public
@typechecked
class NorOp(BoolBinaryOp):
    """AST class for logical NOR operation."""

    kind = ASTKind.NorOpKind
    op_code = "nor"

    def __init__(
        self,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Instantiate AST class for logical NOR operation."""
        super().__init__(
            op_code=self.op_code,
            lhs=lhs,
            rhs=rhs,
            loc=loc,
            parent=parent,
        )


@public
@typechecked
class XnorOp(BoolBinaryOp):
    """AST class for logical XNOR operation."""

    kind = ASTKind.XnorOpKind
    op_code = "xnor"

    def __init__(
        self,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Instantiate AST class for logical XNOR operation."""
        super().__init__(
            op_code=self.op_code,
            lhs=lhs,
            rhs=rhs,
            loc=loc,
            parent=parent,
        )


@public
@typechecked
class NotOp(BoolUnaryOp):
    """AST class for logical NOT operation."""

    kind = ASTKind.NotOpKind
    op_code = "not"

    def __init__(
        self,
        operand: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Instantiate AST class for logical NOT operation."""
        super().__init__(
            op_code=self.op_code,
            operand=operand,
            loc=loc,
            parent=parent,
        )
