"""Module for different kind of ASTx blocks."""

from __future__ import annotations

from typing import cast

from public import public

from astx.base import AST, Expr, ReprStruct, SourceLocation


@public
class Block(AST):
    """The AST tree."""

    name: str
    nodes: list[AST]
    position: int = 0

    def __init__(
        self,
        name: str = "entry",
        loc: SourceLocation = SourceLocation(0, 0),
    ) -> None:
        """Initialize the AST instance."""
        super().__init__(loc=loc)
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
