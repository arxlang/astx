"""Tests for control flow statements."""

import astx

from astx import ASTKind
from astx.viz import visualize


def test_list_comprehension() -> None:
    """Test ListComprehension."""
    list_compre = astx.ListComprehension(
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
    print(list_compre)
    repr(list_compre)
    assert str(list_compre)
    assert list_compre.get_struct()
    assert list_compre.get_struct(simplified=True)
    visualize(list_compre.get_struct())


def test_generator_expr() -> None:
    """Test `GeneratorExpr` class with conditions of Iterable type."""
    comp_1 = astx.ComprehensionClause(
        target=astx.Variable("x"),
        iterable=astx.Variable("my_list"),
        conditions=[
            astx.BoolBinaryOp(
                op_code="==",
                lhs=astx.BinaryOp(
                    op_code="%",
                    lhs=astx.Variable("x"),
                    rhs=astx.LiteralInt32(2),
                ),
                rhs=astx.LiteralInt32(1),
            )
        ],
    )
    comp_2 = astx.ComprehensionClause(
        target=astx.Variable("y"),
        iterable=astx.Variable("my_list"),
        conditions=[
            astx.BoolBinaryOp(
                op_code="==",
                lhs=astx.BinaryOp(
                    op_code="%",
                    lhs=astx.Variable("y"),
                    rhs=astx.LiteralInt32(2),
                ),
                rhs=astx.LiteralInt32(0),
            )
        ],
    )
    gen_expr = astx.GeneratorExpr(
        element=astx.BinaryOp(
            op_code="+", lhs=astx.Variable("x"), rhs=astx.Variable("y")
        ),
        generators=[comp_1, comp_2],
    )
    print(gen_expr)
    print(repr(gen_expr))
    assert str(gen_expr)
    assert gen_expr.get_struct()
    assert gen_expr.get_struct(simplified=True)
    visualize(gen_expr.get_struct())


def test_set_comprehension() -> None:
    """Test SetComprehension."""
    set_comp = astx.SetComprehension(
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
                        rhs=astx.LiteralInt32(10),
                    ),
                    astx.BinaryOp(
                        op_code="<",
                        lhs=astx.Variable("x"),
                        rhs=astx.LiteralInt32(20),
                    ),
                ],
            )
        ],
    )

    assert str(set_comp) == "SET-COMPREHENSION"
    assert set_comp.kind == ASTKind.SetComprehensionKind
    assert set_comp.get_struct()
    assert set_comp.get_struct(simplified=True)
