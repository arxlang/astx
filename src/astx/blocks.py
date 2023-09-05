"""Module for different kind of ASTx blocks."""
from __future__ import annotations

from typing import cast

from public import public

from astx.base import AST, ASTKind, Expr, ReprStruct


@public
class Block(AST):
    """The AST tree."""

    name: str
    nodes: list[AST]
    position: int = 0

    def __init__(self, name: str = "entry") -> None:
        """Initialize the AST instance."""
        super().__init__()
        self.name = name
        self.nodes: list[Expr] = []
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

    def get_struct(self) -> ReprStruct:
        """Return the AST structure of the object."""
        block_node = []

        for node in self.nodes:
            block_node.append(node.get_struct())

        return cast(ReprStruct, block_node)


@public
class Module(Block):
    """AST main expression class."""

    name: str

    def __init__(self, name: str = "main") -> None:
        """Initialize the AST instance."""
        super().__init__(name=name)
        self.kind = ASTKind.ModuleKind

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return f"Module[{self.name}]"

    @property
    def block(self) -> list[AST]:
        """Define an alias for self.nodes."""
        return self.nodes

    def get_struct(self) -> ReprStruct:
        """Return the AST structure of the object."""
        block_node = []

        for node in self.nodes:
            block_node.append(node.get_struct())

        module_node = {f"MODULE[{self.name}]": block_node}

        return cast(ReprStruct, module_node)
