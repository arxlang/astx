"""
This module aims to offer a simple symbol table class.

The `SymbolTable` class offered here allows the definition
of scopes, so the variable or function would be available in
specifics scopes.

"""
from __future__ import annotations

from typing import Dict, Optional, Type

from public import public

from astx.mixes import NamedExpr


@public
class ScopeNodeBase:
    name: str
    parent: Optional[ScopeNodeBase]
    default_parent: Optional[ScopeNodeBase] = None
    named_expr: Dict[str, NamedExpr]

    def __init__(self, name: str, parent=None):
        self.parent: Optional[ScopeNodeBase] = (
            parent or ScopeNodeBase.default_parent
        )
        self.name: str = name
        self.named_expr: Dict[str, NamedExpr] = {}


@public
class ScopeNode(ScopeNodeBase):
    ...


@public
class Scope:
    nodes: Dict[int, ScopeNodeBase]
    current: Optional[ScopeNodeBase]
    previous: Optional[ScopeNodeBase]
    scope_node_class: Type[ScopeNodeBase]

    def __init__(
        self,
        scope_node_class: Type[ScopeNodeBase] = ScopeNode,
    ) -> None:
        self.nodes: Dict[int, ScopeNodeBase] = {}
        self.current = None
        self.previous = None
        self.scope_node_class = scope_node_class

        self.add(self.scope_node_class("root"))

        self.scope_node_class.default_parent = self.current

    def add(self, name, parent=None, change_current=True):
        node = self.scope_node_class(name, parent)

        # The use of id(node) as keys in the nodes dictionary is generally
        # fine, but be aware that this approach may lead to potential issues
        # if the id() of a node is reused after its destruction. It's #
        # unlikely to happen in your current code, but it's something to be aware of.
        self.nodes[id(node)] = node

        if len(self.nodes) == 1 or change_current:
            self.previous = self.current
            self.current = self.nodes[id(node)]

        return node

    def get_first(self) -> ScopeNodeBase:
        return self.nodes[0]

    def get_last(self) -> ScopeNodeBase:
        return self.nodes[-1]

    def destroy(self, node: ScopeNodeBase) -> None:
        del self.nodes[id(node)]
        self.current = self.previous
        self.previous = None

    def set_default_parent(self, node: ScopeNodeBase) -> None:
        self.scope_node_class.default_parent = node


@public
class SymbolTable:
    scopes: Scope

    def __init__(self):
        self.scopes = Scope()

    def define(self, expr: NamedExpr) -> None:
        if not self.scopes.current:
            raise Exception("SymbolTable: No scope active.")
        self.scopes.current.named_expr[expr.name] = expr

    def update(self, expr: NamedExpr) -> None:
        """
        Update the expression on the SymbolTable.

        It is useful mainly for updating the comment of the expression.
        """
        if not self.scopes.current:
            raise Exception("SymbolTable: No scope active.")
        if not expr.name in self.scopes.current.named_expr:
            raise Exception("This name doesn't exist in the SymbolTable.")
        self.scopes.current.named_expr[expr.name] = expr

    def lookup(self, name) -> NamedExpr:
        scope = self.scopes.current
        while scope is not None:
            if name in scope.named_expr:
                return scope.named_expr[name]
            scope = scope.parent
        raise NameError(f"Name '{name}' is not defined")
