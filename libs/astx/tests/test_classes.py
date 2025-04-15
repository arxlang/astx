"""Tests for classes statements."""

from astx.base import DataType
from astx.blocks import Block
from astx.callables import Argument, Arguments, FunctionDef, FunctionPrototype
from astx.classes import (
    ClassDeclStmt,
    ClassDefStmt,
    EnumDeclStmt,
    InterfaceDefStmt,
    StructDeclStmt,
    StructDefStmt,
)
from astx.literals import LiteralInt32
from astx.modifiers import VisibilityKind
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

    method = FunctionDef(
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


def test_enum_decl() -> None:
    """Test `EnumDeclStmt` class."""
    # Enum attributes
    var_r = VariableDeclaration(
        name="RED",
        type_=DataType(),
        value=LiteralInt32(1),
    )

    var_g = VariableDeclaration(
        name="GREEN",
        type_=DataType(),
        value=LiteralInt32(2),
    )

    var_b = VariableDeclaration(
        name="BLUE",
        type_=DataType(),
        value=LiteralInt32(3),
    )

    # Create an enum declaration
    enum_decl = EnumDeclStmt(
        name="Color",
        attributes=[var_r, var_g, var_b],
    )

    assert str(enum_decl)
    assert enum_decl.get_struct()
    assert enum_decl.get_struct(simplified=True)
    visualize(enum_decl.get_struct())


def test_struct_decl() -> None:
    """Test `StructDeclStmt` class."""
    # Define struct attributes
    attr1 = VariableDeclaration(name="id", type_=DataType())
    attr2 = VariableDeclaration(name="value", type_=DataType())

    # create decorator
    decorator1 = Variable(name="decorator_one")

    # Create struct declaration
    struct_decl = StructDeclStmt(
        name="DataPoint",
        attributes=[attr1, attr2],
        decorators=[decorator1],
    )

    assert str(struct_decl)
    assert struct_decl.get_struct()
    assert struct_decl.get_struct(simplified=True)
    visualize(struct_decl.get_struct())


def test_struct_def() -> None:
    """Test `StructDefStmt` class."""
    # Define struct fields
    attr1 = VariableDeclaration(name="id", type_=DataType())

    attr2 = VariableDeclaration(name="value", type_=DataType())

    # create decorator
    decorator1 = Variable(name="decorator_one")

    # Create struct declaration
    struct_def = StructDefStmt(
        name="DataPoint",
        attributes=[attr1, attr2],
        decorators=[decorator1],
    )

    assert str(struct_def)
    assert struct_def.get_struct()
    assert struct_def.get_struct(simplified=True)
    visualize(struct_def.get_struct())


def test_interface_def_stmt() -> None:
    """Test `InterfaceDefStmt` class."""
    decorator1 = Variable(name="MarkerInterface")
    base1 = Variable(name="Iterable")
    attr1 = VariableDeclaration(
        name="MAX_SIZE", type_=DataType(), value=LiteralInt32(100)
    )
    method_proto = FunctionPrototype(
        name="process",
        args=Arguments(*[Argument(name="data", type_=AnyType())]),
        return_type=AnyType(),
    )
    method1 = FunctionDef(prototype=method_proto, body=Block())

    interface_def_stmt = InterfaceDefStmt(
        name="MyInterface",
        bases=[base1],
        decorators=[decorator1],
        attributes=[attr1],
        methods=[method1],
        visibility=VisibilityKind.public,
    )

    print(f"\nGenerated __str__ for InterfaceDefStmt:\n{interface_def_stmt!s}")

    assert str(interface_def_stmt)
    struct = interface_def_stmt.get_struct()
    assert struct

    assert isinstance(struct, dict), (
        "get_struct should return a dict for InterfaceDefStmt"
    )
    expected_key = "INTERFACE-DEF-STMT[+MyInterface]"
    assert expected_key in struct, (
        f"Expected key '{expected_key}' not found in struct: {struct}"
    )

    struct_simplified = interface_def_stmt.get_struct(simplified=True)
    assert struct_simplified
    assert isinstance(struct_simplified, dict), (
        "Simplified struct should be a dict"
    )
    assert expected_key in struct_simplified, (
        f"Expected key '{expected_key}' not found in "
        f"simplified struct: {struct_simplified}"
    )

    visualize(struct)
