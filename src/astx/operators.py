"""ASTx operators."""
from public import public

from astx import datatypes as dts
from astx.base import ASTKind, DataType, ExprType, OperatorType, SourceLocation


@public
class UnaryOp(OperatorType):
    """AST class for the unary operator."""

    def __init__(
        self,
        op_code: str,
        operand: DataType,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the UnaryOp instance."""
        super().__init__()
        self.loc = loc
        self.op_code = op_code
        self.operand = operand
        self.kind = ASTKind.UnaryOpKind


@public
class BinaryOp(OperatorType):
    """AST class for the binary operator."""

    type_: ExprType

    def __init__(
        self,
        op_code: str,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the BinaryOp instance."""
        super().__init__()

        self.loc = loc
        self.op_code = op_code
        self.lhs = lhs
        self.rhs = rhs
        self.kind = ASTKind.BinaryOpKind

        if not (
            issubclass(lhs.type_, dts.Number)
            and issubclass(lhs.type_, dts.Number)
        ):
            raise Exception(
                "For now, binary operators are just allowed for numbers."
                f"LHS: {lhs.type_}, RHS: {rhs.type_}"
            )

        if lhs.type_ == rhs.type_:
            self.type_ = lhs.type_
        else:
            # inference
            self.type_ = max([lhs.type_, rhs.type_], key=lambda v: v.nbytes)
