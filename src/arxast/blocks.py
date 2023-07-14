from typing import List

from arxast.base import AST, ASTKind


class Block(AST):
    """The AST tree."""

    nodes: List[AST]

    def __init__(self) -> None:
        """Initialize the Block instance."""
        super().__init__()
        self.nodes: List[AST] = []

class Module(Block):
    """AST main expression class."""

    name: str

    def __init__(self, name: str) -> None:
        """Initialize the AST instance."""
        super().__init__()
        self.name = name
        self.kind = ASTKind.ModuleKind
