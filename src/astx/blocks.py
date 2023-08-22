"""Module for different kind of ASTx blocks."""
from __future__ import annotations

from typing import List

from public import public

from astx.base import AST, ASTKind, Expr


@public
class Block(AST):
    """The AST tree."""

    name: str
    nodes: List[AST]
    position: int = 0

    def __init__(self, name: str = "entry") -> None:
        """Initialize the AST instance."""
        super().__init__()
        self.name = name
        self.nodes: List[Expr] = []
        self.position: int = 0

    def append(self, value: AST) -> None:
        """Append a new node to the stack."""
        self.nodes.append(value)

    def __iter__(self) -> Block:
        """Overload `iter` magic function."""
        return self

    def __next__(self) -> AST:
        """Overload `next` magic function."""
        if self.position >= len(self.nodes):
            raise StopIteration()

        i = self.position
        self.position += 1
        return self.nodes[i]


@public
class Module(Block):
    """AST main expression class."""

    name: str

    def __init__(self, name: str = "main") -> None:
        """Initialize the AST instance."""
        super().__init__(name=name)
        self.kind = ASTKind.ModuleKind
