from arxast.base import OperatorType, ASTKind, Expr, SourceLocation


class UnaryOp(OperatorType):
    """AST class for the unary operator."""

    def __init__(
        self,
        op_code: str,
        operand: Expr,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the UnaryOp instance."""
        self.loc = loc
        self.op_code = op_code
        self.operand = operand
        self.kind = ASTKind.UnaryOpKind


class BinaryOp(OperatorType):
    """AST class for the binary operator."""

    def __init__(
        self,
        op_code: str,
        lhs: Expr,
        rhs: Expr,
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the BinaryOp instance."""
        self.loc = loc
        self.op_code = op_code
        self.lhs = lhs
        self.rhs = rhs
        self.kind = ASTKind.BinaryOpKind
