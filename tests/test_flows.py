from astx.blocks import Block
from astx.flows import IfStmt
from astx.operators import BinaryOp
from astx.datatypes import Int32Literal


def test_if_stmt():
    op = BinaryOp(op_code=">", lhs=Int32Literal(1), rhs=Int32Literal(2))
    then_block = Block()
    IfStmt(condition=op, then=then_block)


def test_for_stmt():
    ...
