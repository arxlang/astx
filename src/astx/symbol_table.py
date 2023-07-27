"""
This module aims to offer a simple symbol table class.

The `SymbolTable` class offered here allows the definition
of scopes, so the variable or function would be available in
specifics scopes.

"""
from __future__ import annotations
from typing import Dict, Optional

from public import public

from astx.mixes import NamedExpr


@public
class ScopeNode:
    name: str
    named_expr: Dict[str, NamedExpr]
    parent: Optional[ScopeNode]
    default_parent: Optional[ScopeNode] = None

    def __init__(self, name: str, parent=None):
        self.named_expr: Dict[str, NamedExpr] = {}
        self.parent: Optional[ScopeNode] = parent or ScopeNode.default_parent
        self.name: str = name


@public
class Scope:
    nodes: Dict[int, ScopeNode]
    current: Optional[ScopeNode]
    previous: Optional[ScopeNode]

    def __init__(self) -> None:
        self.nodes: Dict[int, ScopeNode] = {}
        self.current = None
        self.previous = None

        self.add(ScopeNode("root"))

        ScopeNode.default_parent = self.current

    def add(self, name, parent=None, change_current=True):
        node = ScopeNode(name, parent)

        # The use of id(node) as keys in the nodes dictionary is generally
        # fine, but be aware that this approach may lead to potential issues
        # if the id() of a node is reused after its destruction. It's #
        # unlikely to happen in your current code, but it's something to be aware of.
        self.nodes[id(node)] = node

        if len(self.nodes) == 1 or change_current:
            self.previous = self.current
            self.current = self.nodes[id(node)]

        return node

    def get_first(self) -> ScopeNode:
        return self.nodes[0]

    def get_last(self) -> ScopeNode:
        return self.nodes[-1]

    def destroy(self, node: ScopeNode) -> None:
        del self.nodes[id(node)]
        self.current = self.previous
        self.previous = None

    def set_default_parent(self, node: ScopeNode) -> None:
        ScopeNode.default_parent = node


@public
class SymbolTable:
    scopes: Scope

    def __init__(self):
        self.scopes = Scope()

    def define(self, expr: NamedExpr) -> None:
        if not self.scopes.current:
            raise Exception("SymbolTable: No scope active.")
        self.scopes.current.named_expr[expr.name] = expr

    def lookup(self, name) -> NamedExpr:
        scope = self.scopes.current
        while scope is not None:
            if name in scope.named_expr:
                return scope.named_expr[name]
            scope = scope.parent
        raise NameError(f"Name '{name}' is not defined")
