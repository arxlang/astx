"""Module for testing different kind of ASTx blocks."""

from astx.literals.numeric import LiteralInt32
from astx.packages import (
    AliasExpr,
    ImportExpr,
    ImportFromExpr,
    ImportFromStmt,
    ImportStmt,
    Module,
    Package,
    Program,
    Target,
)
from astx.types.numeric import Int32
from astx.types.operators import BinaryOp
from astx.variables import Variable, VariableDeclaration
from astx.viz import visualize


def test_module() -> None:
    """Test ASTx module."""
    module = Module()

    decl_a = VariableDeclaration("a", type_=Int32(), value=LiteralInt32(1))
    decl_b = VariableDeclaration("b", type_=Int32(), value=LiteralInt32(2))

    var_a = Variable("a")
    var_b = Variable("b")
    sum_op = BinaryOp(op_code="+", lhs=var_a, rhs=var_b)

    module.append(decl_a)
    module.append(decl_b)
    module.append(sum_op)

    assert module.get_struct()
    assert module.get_struct(simplified=True)

    visualize(module.get_struct())


def test_target() -> None:
    """Test ASTx module."""
    target = Target(
        datalayout="e-m:e-i64:64-f80:128-n8:16:32:64-S128",
        triple="x86_64-pc-linux-gnu",
    )

    assert target.get_struct()
    assert target.get_struct(simplified=True)

    visualize(target.get_struct())


def test_packages() -> None:
    """Test ASTx package."""
    package_main = Package()
    package_child = Package()
    module_main = Module()
    module_child = Module()

    package_child.modules.append(module_child)
    package_main.packages.append(package_child)
    package_main.modules.append(module_main)

    assert package_main.get_struct()
    assert package_main.get_struct(simplified=True)

    visualize(package_main.get_struct())


def test_program() -> None:
    """Test ASTx program."""
    target = Target(
        datalayout="e-m:e-i64:64-f80:128-n8:16:32:64-S128",
        triple="x86_64-pc-linux-gnu",
    )

    package_main = Package()
    package_child = Package()
    module_program = Module()
    module_main = Module()
    module_child = Module()
    program = Program(target=target)

    package_child.modules.append(module_child)
    package_main.packages.append(package_child)
    package_main.modules.append(module_main)

    program.packages.append(package_main)
    program.modules.append(module_program)

    assert program.get_struct()
    assert program.get_struct(simplified=True)

    visualize(program.get_struct())


def test_multiple_imports_stmt() -> None:
    """Test ImportStmt multiple imports."""
    alias1 = AliasExpr(name="math")
    alias2 = AliasExpr(name="matplotlib", asname="mtlb")

    # Create an import statement
    import_stmt = ImportStmt(names=[alias1, alias2])

    assert import_stmt.get_struct()
    assert import_stmt.get_struct(simplified=True)


def test_import_from_stmt() -> None:
    """Test ImportFromStmt importing from module."""
    alias = AliasExpr(name="pyplot", asname="plt")

    import_from_stmt = ImportFromStmt(
        module="matplotlib", names=[alias], level=1
    )

    assert import_from_stmt.get_struct()
    assert import_from_stmt.get_struct(simplified=True)


def test_wildcard_import_from_stmt() -> None:
    """Test ImportFromStmt wildcard import from module."""
    alias = AliasExpr(name="*")

    import_from_stmt = ImportFromStmt(module="matplotlib", names=[alias])

    assert import_from_stmt.get_struct()
    assert import_from_stmt.get_struct(simplified=True)


def test_future_import_from_stmt() -> None:
    """Test ImportFromStmt from future import."""
    alias = AliasExpr(name="division")

    import_from_stmt = ImportFromStmt(module="__future__", names=[alias])
    assert import_from_stmt.get_struct()
    assert import_from_stmt.get_struct(simplified=True)


def test_multiple_imports_expr() -> None:
    """Test ImportExpr multiple imports."""
    alias1 = AliasExpr(name="sqrt", asname="square_root")
    alias2 = AliasExpr(name="pi")

    import_expr = ImportExpr([alias1, alias2])

    assert import_expr.get_struct()
    assert import_expr.get_struct(simplified=True)


def test_import_from_expr() -> None:
    """Test ImportFromExpr importing from module."""
    alias1 = AliasExpr(name="sqrt", asname="square_root")

    import_from_expr = ImportFromExpr(module="math", names=[alias1])

    assert import_from_expr.get_struct()
    assert import_from_expr.get_struct(simplified=True)


def test_wildcard_import_from_expr() -> None:
    """Test ImportFromExpr wildcard import from module."""
    alias1 = AliasExpr(name="*")

    import_from_expr = ImportFromExpr(module="math", names=[alias1])

    assert import_from_expr.get_struct()
    assert import_from_expr.get_struct(simplified=True)


def test_future_import_from_expr() -> None:
    """Test ImportFromExpr from future import."""
    alias1 = AliasExpr(name="division")

    import_from_expr = ImportFromExpr(module="__future__", names=[alias1])

    assert import_from_expr.get_struct()
    assert import_from_expr.get_struct(simplified=True)


def test_relative_import_from_expr() -> None:
    """Test ImportFromExpr relative imports."""
    alias1 = AliasExpr(name="division")
    alias2 = AliasExpr(name="matplotlib", asname="mtlb")

    import_from_expr = ImportFromExpr(names=[alias1, alias2], level=1)

    assert import_from_expr.get_struct()
    assert import_from_expr.get_struct(simplified=True)
