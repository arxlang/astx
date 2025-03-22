"""Module for different kind of ASTx blocks."""

from __future__ import annotations

from typing import cast

from public import public

from astx.base import (
    ASTNodes,
    ASTType,
    ReprStruct,
)
from astx.tools.typing import typechecked


@public
@typechecked
class Block(ASTNodes[ASTType]):
    """The AST tree."""

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        block_nodes = []

        for node in self.nodes:
            block_nodes.append(node.get_struct(simplified))

        key = f"BLOCK[{self.name}-{id(self)}]"
        value = cast(ReprStruct, block_nodes)

        return self._prepare_struct(key, value, simplified)
