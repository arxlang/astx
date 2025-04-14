"""ASTx Collection Objects."""

from __future__ import annotations

from typing import Dict, List, Optional, Set, Tuple, cast

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    ReprStruct,
    SourceLocation,
)
from astx.literals import Literal
from astx.tools.typing import typechecked
from astx.types.operators import DataTypeOps


@public
@typechecked
class ObjectList(DataTypeOps):
    """Object Representation of list."""

    elements: List[DataTypeOps]

    def __init__(
        self,
        elements: List[DataTypeOps],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize LiteralList."""
        super().__init__(loc, parent)
        self.elements = elements
        self.kind = ASTKind.ObjectListKind

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return f"{self.__class__.__name__}"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the string representation of the object."""
        key = "OBJECT-LIST"
        value: ReprStruct = cast(
            ReprStruct,
            [
                str(element)
                if isinstance(element, Literal)
                else element.get_struct(simplified)
                for element in self.elements
            ],
        )
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class ObjectTuple(DataTypeOps):
    """Object Representation of Tuple."""

    elements: Tuple[DataTypeOps, ...]

    def __init__(
        self,
        elements: Tuple[DataTypeOps, ...],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize LiteralList."""
        super().__init__(loc, parent)
        self.elements = elements
        self.kind = ASTKind.ObjectTupleKind

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return f"{self.__class__.__name__}"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the string representation of the object."""
        key = "OBJECT-TUPLE"
        value: ReprStruct = cast(
            ReprStruct,
            [
                str(element)
                if isinstance(element, Literal)
                else element.get_struct(simplified)
                for element in self.elements
            ],
        )
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class ObjectSet(DataTypeOps):
    """Object Representation of Set."""

    elements: Set[DataTypeOps]

    def __init__(
        self,
        elements: Set[DataTypeOps],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize LiteralList."""
        super().__init__(loc, parent)
        self.elements = elements
        self.kind = ASTKind.ObjectSetKind

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return f"{self.__class__.__name__}"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the string representation of the object."""
        key = "OBJECT-SET"
        value: ReprStruct = cast(
            ReprStruct,
            [
                str(element)
                if isinstance(element, Literal)
                else element.get_struct(simplified)
                for element in self.elements
            ],
        )
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class ObjectDict(DataTypeOps):
    """Object Representation of Dict."""

    elements: Dict[DataTypeOps, DataTypeOps]

    def __init__(
        self,
        elements: Dict[DataTypeOps, DataTypeOps],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize LiteralList."""
        super().__init__(loc, parent)
        self.elements = elements
        self.kind = ASTKind.ObjectDictKind

    def __str__(self) -> str:
        """Return the string representation of the object."""
        return f"{self.__class__.__name__}"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the string representation of the object."""
        key = "OBJECT-DICT"
        value: ReprStruct = cast(
            ReprStruct,
            [
                (
                    f"{
                        str(key)
                        if isinstance(key, Literal)
                        else key.get_struct(simplified)
                    }:"
                    f"{
                        str(val)
                        if isinstance(val, Literal)
                        else val.get_struct(simplified)
                    }"
                )
                for key, val in self.elements.items()
            ],
        )
        return self._prepare_struct(key, value, simplified)
