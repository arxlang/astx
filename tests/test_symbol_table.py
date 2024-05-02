"""Test classes and functions about Symbol Table."""

from astx import Variable
from astx.symbol_table import SymbolTable


def test_symbol_table() -> None:
    """Test SymbolTable class."""
    symtable = SymbolTable()

    var_a = Variable("var_a")

    symtable.define(var_a)
    symtable.update(var_a)
    symtable.lookup("var_a")


def test_scope() -> None:
    """Test Scope class."""
    symtable = SymbolTable()

    var_a = Variable("var_a")

    symtable.define(var_a)
    symtable.update(var_a)
    symtable.lookup("var_a")

    scope = symtable.scopes

    scope.add("var_b")
    scope.get_first()
    scope.get_last()
