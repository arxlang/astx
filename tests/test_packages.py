"""Module for testing different kind of ASTx blocks."""

from astx.datatypes import Int32, LiteralInt32
from astx.operators import BinaryOp
from astx.packages import Module, Package, Program, Target
from astx.variables import Variable, VariableDeclaration
from astx.viz import visualize


def test_module() -> None:
    """Test ASTx module."""
    module = Module()

    decl_a = VariableDeclaration("a", type_=Int32, value=LiteralInt32(1))
    decl_b = VariableDeclaration("b", type_=Int32, value=LiteralInt32(2))

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
