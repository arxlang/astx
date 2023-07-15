from arxast.blocks import Block
from arxast.statements import IfStmt, ForStmt
from arxast.operators import BinaryOp
from arxast.datatypes import Int32Literal


def test_if_stmt():
    op = BinaryOp(op_code=">", lhs=Int32Literal(1), rhs=Int32Literal(2))
    then_block = Block()
    if_stmt = IfStmt(condition=op, then=then_block)


def test_for_stmt():
    ...
