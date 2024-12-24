"""Tests for classes statements."""

from astx.base import DataType
from astx.blocks import Block
from astx.callables import Arguments, Function, FunctionPrototype
from astx.classes import ClassDeclStmt, ClassDefStmt
from astx.literals import LiteralInt32
from astx.types.base import AnyType
from astx.variables import Variable, VariableDeclaration
from astx.viz import visualize


def test_class_decl() -> None:
    """Test `ClassDeclStmt` class."""
    # Decorators
    decorator1 = Variable(name="decorator_one")

    # Create a class declaration
    class_decl = ClassDeclStmt(
        name="MyClass",
        decorators=[decorator1],
        is_abstract=True,
    )

    assert str(class_decl)
    assert class_decl.get_struct()
    assert class_decl.get_struct(simplified=True)
    visualize(class_decl.get_struct())


def test_class_def() -> None:
    """Test `ClassDefStmt` class."""
    # class attribute
    var_decl = VariableDeclaration(
        name="my_variable",
        type_=DataType(),
        value=LiteralInt32(10),
    )

    # class method
    prototype = FunctionPrototype(
        name="my_method",
        args=Arguments(),
        return_type=AnyType(),
    )

    method = Function(
        prototype=prototype,
        body=Block(),
    )

    # Create a class definition
    class_def = ClassDefStmt(
        name="MyClass",
        attributes=[var_decl],
        methods=[method],
    )

    assert str(class_def)
    assert class_def.get_struct()
    assert class_def.get_struct(simplified=True)
    visualize(class_def.get_struct())
