"""Tests for control flow statements."""

import astx

from astx.viz import visualize


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
