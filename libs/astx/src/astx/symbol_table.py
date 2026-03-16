"""
title: Symbol Table module for ASTx.
summary: |-

  The `SymbolTable` class offered here allows the definition
  of scopes, so the variable or function would be available in
  specifics scopes.
"""

from __future__ import annotations

from typing import Optional

from public import public

from astx.mixes import NamedExpr
from astx.tools.typing import typechecked


@public
@typechecked
class ScopeNodeBase:
    """
    title: ScopeNodeBase is the base used for the nodes (levels) in the scope.
    attributes:
      name:
        type: str
      parent:
        type: Optional[ScopeNodeBase]
      default_parent:
        type: Optional[ScopeNodeBase]
      named_expr:
        type: dict[str, NamedExpr]
    """

    name: str
    parent: Optional[ScopeNodeBase]
    default_parent: Optional[ScopeNodeBase] = None
    named_expr: dict[str, NamedExpr]

    def __init__(
        self, name: str, parent: Optional[ScopeNodeBase] = None
    ) -> None:
        """
        title: Initialize ScopeNodeBase.
        parameters:
          name:
            type: str
          parent:
            type: Optional[ScopeNodeBase]
        """
        self.parent: Optional[ScopeNodeBase] = (
            parent or ScopeNodeBase.default_parent
        )
        self.name: str = name
        self.named_expr: dict[str, NamedExpr] = {}


@public
@typechecked
class ScopeNode(ScopeNodeBase):
    """
    title: Scope node organize the scope in different levels in the stack.
    attributes:
      name:
        type: str
      parent:
        type: Optional[ScopeNodeBase]
      default_parent:
        type: Optional[ScopeNodeBase]
      named_expr:
        type: dict[str, NamedExpr]
    """

    ...


@public
@typechecked
class Scope:
    """
    title: Organize the ASTx objects according to the scope.
    attributes:
      nodes:
        type: dict[int, ScopeNodeBase]
      current:
        type: Optional[ScopeNodeBase]
      previous:
        type: Optional[ScopeNodeBase]
      scope_node_class:
        type: type[ScopeNodeBase]
    """

    nodes: dict[int, ScopeNodeBase]
    current: Optional[ScopeNodeBase]
    previous: Optional[ScopeNodeBase]
    scope_node_class: type[ScopeNodeBase]

    def __init__(
        self,
        scope_node_class: type[ScopeNodeBase] = ScopeNode,
    ) -> None:
        """
        title: Initialize the scope.
        parameters:
          scope_node_class:
            type: type[ScopeNodeBase]
        """
        self.nodes: dict[int, ScopeNodeBase] = {}
        self.current = None
        self.previous = None
        self.scope_node_class = scope_node_class

        self.add("root")

        self.scope_node_class.default_parent = self.current

    def add(
        self,
        name: str,
        parent: Optional[ScopeNodeBase] = None,
        change_current: bool = True,
    ) -> ScopeNodeBase:
        """
        title: Add a new node in the scope.
        parameters:
          name:
            type: str
          parent:
            type: Optional[ScopeNodeBase]
          change_current:
            type: bool
        returns:
          type: ScopeNodeBase
        """
        node = self.scope_node_class(name, parent)

        # The use of id(node) as keys in the nodes dictionary is generally
        # fine, but be aware that this approach may lead to potential issues
        # if the id() of a node is reused after its destruction. It's #
        # unlikely to happen in the current code, but it's something to be
        # aware of.
        self.nodes[id(node)] = node

        if len(self.nodes) == 1 or change_current:
            self.previous = self.current
            self.current = self.nodes[id(node)]

        return node

    def get_first(self) -> ScopeNodeBase:
        """
        title: Get the first node in the scope.
        returns:
          type: ScopeNodeBase
        """
        node_id = next(iter(self.nodes.keys()))
        return self.nodes[node_id]

    def get_last(self) -> ScopeNodeBase:
        """
        title: Get the latest node in the scope.
        returns:
          type: ScopeNodeBase
        """
        node_id = list(self.nodes.keys())[-1]
        return self.nodes[node_id]

    def destroy(self, node: ScopeNodeBase) -> None:
        """
        title: Destroy the current scope.
        parameters:
          node:
            type: ScopeNodeBase
        """
        del self.nodes[id(node)]
        self.current = self.previous
        self.previous = None

    def set_default_parent(self, node: ScopeNodeBase) -> None:
        """
        title: Set default parent for the current scope.
        parameters:
          node:
            type: ScopeNodeBase
        """
        self.scope_node_class.default_parent = node


@public
@typechecked
class SymbolTable:
    """
    title: Symbol Table for ASTx.
    attributes:
      scopes:
        type: Scope
    """

    scopes: Scope

    def __init__(self) -> None:
        self.scopes = Scope()

    def define(self, expr: NamedExpr) -> None:
        """
        title: Define a new named expression inside the scoped stack.
        parameters:
          expr:
            type: NamedExpr
        """
        if not self.scopes.current:
            raise Exception("SymbolTable: No scope active.")
        self.scopes.current.named_expr[expr.name] = expr

    def update(self, expr: NamedExpr) -> None:
        """
        title: Update the expression on the SymbolTable.
        summary: |-

          It is useful mainly for updating the comment of the expression.
        parameters:
          expr:
            type: NamedExpr
        """
        if not self.scopes.current:
            raise Exception("SymbolTable: No scope active.")
        if expr.name not in self.scopes.current.named_expr:
            raise Exception("This name doesn't exist in the SymbolTable.")
        self.scopes.current.named_expr[expr.name] = expr

    def lookup(self, name: str) -> NamedExpr:
        """
        title: Get a named expression from the scope stack.
        parameters:
          name:
            type: str
        returns:
          type: NamedExpr
        """
        scope = self.scopes.current
        while scope is not None:
            if name in scope.named_expr:
                return scope.named_expr[name]
            scope = scope.parent
        raise NameError(f"Name '{name}' is not defined")
