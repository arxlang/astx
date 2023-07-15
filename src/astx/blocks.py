from __future__ import annotations
from typing import List

from astx.base import AST, Expr, ASTKind


class Block(AST):
    """The AST tree."""

    nodes: List[Expr]
    position: int = 0

    def __init__(self):
        self.nodes: List[Expr] = []
        self.position: int = 0

    def append(self, value: Expr):
        self.nodes.append(value)

    def __iter__(self) -> Block:
        return self

    def __next__(self) -> Expr:
        if self.position >= len(self.nodes):
            raise StopIteration()

        i = self.position
        self.position += 1
        return self.nodes[i]


class Module(Block):
    """AST main expression class."""

    name: str

    def __init__(self, name: str = "main") -> None:
        """Initialize the AST instance."""
        super().__init__()
        self.name = name
        self.kind = ASTKind.ModuleKind
