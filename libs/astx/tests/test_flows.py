"""Tests for control flow statements."""

import astx
import pytest

from astx.base import SourceLocation
from astx.blocks import Block
from astx.flows import (
    AsyncForRangeLoopExpr,
    AsyncForRangeLoopStmt,
    CaseStmt,
    DoWhileExpr,
    DoWhileStmt,
    ForCountLoopExpr,
    ForCountLoopStmt,
    ForRangeLoopExpr,
    ForRangeLoopStmt,
    IfExpr,
    IfStmt,
    SwitchStmt,
    WhileExpr,
    WhileStmt,
)
from astx.literals import LiteralInt32, LiteralString
from astx.literals.numeric import LiteralInt32
from astx.types.numeric import Int32
from astx.types.operators import BinaryOp, UnaryOp
from astx.variables import InlineVariableDeclaration, Variable
from astx.viz import visualize


def test_if_stmt() -> None:
    """Test `if` statement."""
    op = BinaryOp(op_code=">", lhs=LiteralInt32(1), rhs=LiteralInt32(2))
    then_block = Block()
    if_stmt = IfStmt(condition=op, then=then_block)

    assert str(if_stmt)
    assert if_stmt.get_struct()
    assert if_stmt.get_struct(simplified=True)
    visualize(if_stmt.get_struct())


def test_if_else_stmt() -> None:
    """Test `if`/`else` statement."""
    cond = BinaryOp(op_code=">", lhs=LiteralInt32(1), rhs=LiteralInt32(2))
    then_block = Block()
    else_block = Block()
    if_stmt = IfStmt(condition=cond, then=then_block, else_=else_block)

    assert str(if_stmt)
    assert if_stmt.get_struct()
    assert if_stmt.get_struct(simplified=True)
    visualize(if_stmt.get_struct())


def test_if_expr() -> None:
    """Test `if` expression."""
    op = BinaryOp(op_code=">", lhs=LiteralInt32(1), rhs=LiteralInt32(2))
    then_block = Block()
    if_expr = IfExpr(condition=op, then=then_block)

    assert str(if_expr)
    assert if_expr.get_struct()
    assert if_expr.get_struct(simplified=True)
    visualize(if_expr.get_struct())


def test_if_else_expr() -> None:
    """Test `if`/`else` expression."""
    cond = BinaryOp(op_code=">", lhs=LiteralInt32(1), rhs=LiteralInt32(2))
    then_block = Block()
    else_block = Block()
    if_expr = IfExpr(condition=cond, then=then_block, else_=else_block)

    assert str(if_expr)
    assert if_expr.get_struct()
    assert if_expr.get_struct(simplified=True)
    visualize(if_expr.get_struct())


def test_for_range_loop_expr() -> None:
    """Test `For Range Loop` expression`."""
    decl_a = InlineVariableDeclaration(
        "a", type_=Int32(), value=LiteralInt32(-1)
    )
    start = LiteralInt32(1)
    end = LiteralInt32(10)
    step = LiteralInt32(1)
    body = Block()
    body.append(LiteralInt32(2))
    for_expr = ForRangeLoopExpr(
        variable=decl_a, start=start, end=end, step=step, body=body
    )

    assert str(for_expr)
    assert for_expr.get_struct()
    assert for_expr.get_struct(simplified=True)
    visualize(for_expr.get_struct())


def test_for_range_loop_stmt() -> None:
    """Test `For Range Loop` statement."""
    decl_a = InlineVariableDeclaration(
        "a", type_=Int32(), value=LiteralInt32(-1)
    )
    start = LiteralInt32(1)
    end = LiteralInt32(10)
    step = LiteralInt32(1)
    body = Block()
    body.append(LiteralInt32(2))
    for_stmt = ForRangeLoopStmt(
        variable=decl_a, start=start, end=end, step=step, body=body
    )

    assert str(for_stmt)
    assert for_stmt.get_struct()
    assert for_stmt.get_struct(simplified=True)
    visualize(for_stmt.get_struct())


def test_for_count_loop_stmt() -> None:
    """Test `For Count Loop` statement."""
    decl_a = InlineVariableDeclaration(
        "a", type_=Int32(), value=LiteralInt32(0)
    )
    var_a = Variable("a")
    cond = BinaryOp(op_code="<", lhs=var_a, rhs=LiteralInt32(10))
    update = UnaryOp(op_code="++", operand=var_a)
    body = Block()
    body.append(LiteralInt32(2))
    for_stmt = ForCountLoopStmt(
        initializer=decl_a, condition=cond, update=update, body=body
    )

    assert str(for_stmt)
    assert for_stmt.get_struct()
    assert for_stmt.get_struct(simplified=True)
    visualize(for_stmt.get_struct())


def test_for_count_loop_expr() -> None:
    """Test `For Count Loop` expression."""
    decl_a = InlineVariableDeclaration(
        "a", type_=Int32(), value=LiteralInt32(0)
    )
    var_a = Variable("a")
    cond = BinaryOp(op_code="<", lhs=var_a, rhs=LiteralInt32(10))
    update = UnaryOp(op_code="++", operand=var_a)
    body = Block()
    body.append(LiteralInt32(2))
    for_expr = ForCountLoopExpr(
        initializer=decl_a, condition=cond, update=update, body=body
    )

    assert str(for_expr)
    assert for_expr.get_struct()
    assert for_expr.get_struct(simplified=True)
    visualize(for_expr.get_struct())


def test_async_for_range_loop_expr() -> None:
    """Test `Async For Range Loop` expression`."""
    decl_a = InlineVariableDeclaration(
        "a", type_=Int32(), value=LiteralInt32(-1)
    )
    start = LiteralInt32(1)
    end = LiteralInt32(10)
    step = LiteralInt32(1)
    body = Block()
    body.append(LiteralInt32(2))
    for_expr = AsyncForRangeLoopExpr(
        variable=decl_a, start=start, end=end, step=step, body=body
    )

    assert str(for_expr)
    assert for_expr.get_struct()
    assert for_expr.get_struct(simplified=True)
    visualize(for_expr.get_struct())


def test_async_for_range_loop_stmt() -> None:
    """Test `Async For Range Loop` statement."""
    decl_a = InlineVariableDeclaration(
        "a", type_=Int32(), value=LiteralInt32(-1)
    )
    start = LiteralInt32(1)
    end = LiteralInt32(10)
    step = LiteralInt32(1)
    body = Block()
    body.append(LiteralInt32(2))
    for_stmt = AsyncForRangeLoopStmt(
        variable=decl_a, start=start, end=end, step=step, body=body
    )

    assert str(for_stmt)
    assert for_stmt.get_struct()
    assert for_stmt.get_struct(simplified=True)
    visualize(for_stmt.get_struct())


def test_while_expr() -> None:
    """Test `WhileExpr` class."""
    # Define a condition: x < 5
    x_var = Variable(name="x")
    condition = BinaryOp(
        op_code="<",
        lhs=x_var,
        rhs=LiteralInt32(5),
        loc=SourceLocation(line=1, col=0),
    )

    body_block = Block(name="while_body")

    # Create the WhileExpr
    while_expr = WhileExpr(
        condition=condition, body=body_block, loc=SourceLocation(line=1, col=0)
    )

    assert str(while_expr)
    assert while_expr.get_struct()
    assert while_expr.get_struct(simplified=True)
    visualize(while_expr.get_struct())


def test_while_stmt() -> None:
    """Test `WhileStmt` class."""
    # Define a condition: x < 5
    x_var = Variable(name="x")
    condition = BinaryOp(
        op_code="<",
        lhs=x_var,
        rhs=LiteralInt32(5),
        loc=SourceLocation(line=1, col=0),
    )

    body_block = Block(name="while_body")

    # Create the WhileStmt
    while_stmt = WhileStmt(
        condition=condition, body=body_block, loc=SourceLocation(line=1, col=0)
    )

    assert str(while_stmt)
    assert while_stmt.get_struct()
    assert while_stmt.get_struct(simplified=True)
    visualize(while_stmt.get_struct())


def test_case_stmt() -> None:
    """Test `CaseStmt` class."""
    condition1 = LiteralInt32(value=1)
    body1 = astx.Block()
    body1.append(LiteralString(value="one"))
    case1 = CaseStmt(condition=condition1, body=body1)

    assert str(case1)
    assert case1.get_struct()
    assert case1.get_struct(simplified=True)
    visualize(case1.get_struct())


def test_case_stmt_error1() -> None:
    """Test `CaseStmt` class for default/condition inconsistency (1)."""
    # should raise error - mustn't have condition since default=True
    with pytest.raises(ValueError):
        condition1 = LiteralInt32(value=1)
        body1 = astx.Block()
        body1.append(LiteralString(value="one"))
        case1 = CaseStmt(  # noqa F841
            default=True,
            condition=condition1,
            body=body1,
        )


def test_case_stmt_error2() -> None:
    """Test `CaseStmt` class for default/condition inconsistency (2)."""
    # should raise error - must have condition since deault=False
    with pytest.raises(ValueError):
        body1 = astx.Block()
        body1.append(LiteralString(value="one"))
        case1 = CaseStmt(body=body1)  # noqa F841


def test_switch_stmt() -> None:
    """Test `SwitchStmt` class."""
    # The expression to match
    value_expr = Variable(name="x")

    # Patterns and corresponding expressions
    condition1 = LiteralInt32(value=1)
    body1 = astx.Block()
    body1.append(LiteralString(value="one"))

    condition2 = LiteralInt32(value=2)
    body2 = astx.Block()
    body2.append(LiteralString(value="two"))

    body_default = astx.Block()
    body2.append(LiteralString(value="other"))

    # create branches
    case1 = CaseStmt(condition=condition1, body=body1)
    case2 = CaseStmt(condition=condition2, body=body2)
    case_default = CaseStmt(default=True, body=body_default)

    # Create the SwitchStmt
    switch_stmt = SwitchStmt(
        value=value_expr,
        cases=[case1, case2, case_default],
    )

    assert str(switch_stmt)
    assert switch_stmt.get_struct()
    assert switch_stmt.get_struct(simplified=True)
    visualize(switch_stmt.get_struct())


def test_goto_stmt() -> None:
    """Test `GotoStmt` class."""
    goto_stmt = astx.GotoStmt(astx.Identifier("label1"))

    assert str(goto_stmt)
    assert goto_stmt.get_struct()
    assert goto_stmt.get_struct(simplified=True)
    visualize(goto_stmt.get_struct())


def test_comprehension() -> None:
    """Test generic comphrehension."""
    target = astx.LiteralString("x")
    iterable = astx.LiteralString("range(10)")
    condition = astx.LiteralString("x > 5")

    comp = astx.ComprehensionClause(
        target=target,
        iterable=iterable,
        conditions=[condition],
        is_async=True,
    )

    expected_str = "COMPREHENSION[is_async=True]"
    assert str(comp) == expected_str
    assert comp.get_struct(simplified=True)
    assert comp.get_struct(simplified=False)


def test_do_while_expr() -> None:
    """Test `DoWhileExpr` class."""
    # Define a condition: x < 5
    x_var = Variable(name="x")
    condition = BinaryOp(
        op_code="<",
        lhs=x_var,
        rhs=LiteralInt32(5),
    )

    body_block = Block(name="do_while_body")

    # Create the DoWhileLoopExpr
    do_while_expr = DoWhileExpr(condition=condition, body=body_block)

    assert str(do_while_expr)
    assert do_while_expr.get_struct()
    assert do_while_expr.get_struct(simplified=True)
    visualize(do_while_expr.get_struct())


def test_do_while_stmt() -> None:
    """Test `DoWhileStmt` class."""
    # Define a condition: x < 5
    x_var = Variable(name="x")
    condition = BinaryOp(
        op_code="<",
        lhs=x_var,
        rhs=LiteralInt32(5),
    )

    body_block = Block(name="do_while_body")

    # Create the DoWhileStmt
    do_while_stmt = DoWhileStmt(condition=condition, body=body_block)

    assert str(do_while_stmt)
    assert do_while_stmt.get_struct()
    assert do_while_stmt.get_struct(simplified=True)
    visualize(do_while_stmt.get_struct())


def test_generator_expr_1() -> None:
    """Test `GeneratorExpr` class with conditions of Iterable type."""
    gen_expr = astx.GeneratorExpr(
        element=astx.BinaryOp(
            op_code="+", lhs=astx.Variable("x"), rhs=astx.Variable("x")
        ),
        target=astx.Variable("x"),
        iterable=astx.Identifier("range(10)"),
        conditions=[
            astx.BinaryOp(
                op_code="<", lhs=astx.Variable("x"), rhs=astx.LiteralInt32(8)
            ),
            astx.BinaryOp(
                op_code="%", lhs=astx.Variable("x"), rhs=astx.LiteralInt32(2)
            ),
        ],
    )
    assert str(gen_expr)
    assert gen_expr.get_struct()
    assert gen_expr.get_struct(simplified=True)
    visualize(gen_expr.get_struct())


def test_generator_expr_2() -> None:
    """Test `GeneratorExpr` class with conditions of ASTNodes type."""
    conditions = astx.ASTNodes[astx.Expr]()
    conditions.append(
        astx.BinaryOp(
            op_code="<", lhs=astx.Variable("x"), rhs=astx.LiteralInt32(8)
        )
    )
    conditions.append(
        astx.BinaryOp(
            op_code="%", lhs=astx.Variable("x"), rhs=astx.LiteralInt32(2)
        )
    )
    gen_expr = astx.GeneratorExpr(
        element=astx.BinaryOp(
            op_code="+", lhs=astx.Variable("x"), rhs=astx.Variable("x")
        ),
        target=astx.Variable("x"),
        iterable=astx.Identifier("range(10)"),
        conditions=conditions,
    )
    print(gen_expr)
    assert str(gen_expr)
    assert gen_expr.get_struct()
    assert gen_expr.get_struct(simplified=True)
    visualize(gen_expr.get_struct())


def test_list_comprehension() -> None:
    """Test ListComprehension."""
    gen_expr = astx.ListComprehension(
        element=astx.BinaryOp(
            op_code="+", lhs=astx.Variable("x"), rhs=astx.Variable("x")
        ),
        generators=[
            astx.ComprehensionClause(
                target=astx.Variable("x"),
                iterable=astx.Identifier("range_10"),
                conditions=[
                    astx.BinaryOp(
                        op_code=">",
                        lhs=astx.Variable("x"),
                        rhs=astx.LiteralInt32(3),
                    ),
                    astx.BinaryOp(
                        op_code="<",
                        lhs=astx.Variable("x"),
                        rhs=astx.LiteralInt32(7),
                    ),
                ],
            )
        ],
    )
    print(gen_expr)
    repr(gen_expr)
    assert str(gen_expr)
    assert gen_expr.get_struct()
    assert gen_expr.get_struct(simplified=True)
    visualize(gen_expr.get_struct())
