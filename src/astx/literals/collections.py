"""ASTx Collection Literals."""

from __future__ import annotations

from typing import Dict, List, Set, Tuple

from public import public

from astx.base import NO_SOURCE_LOCATION, SourceLocation
from astx.literals.base import Literal
from astx.tools.typing import typechecked
from astx.types.collections import DictType, ListType, SetType, TupleType
from astx.types.numeric import Int32


@public
@typechecked
class LiteralList(Literal):
    """Literal representation of a List."""

    elements: List[Literal]

    def __init__(
        self, elements: List[Literal], loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralList."""
        super().__init__(loc)
        self.elements = list(elements)  # Ensure correct type
        unique_types = {type(elem.type_) for elem in elements}
        self.type_ = ListType([t() for t in unique_types])
        self.loc = loc


@public
@typechecked
class LiteralTuple(Literal):
    """Literal representation of a Tuple."""

    elements: Tuple[Literal, ...]

    def __init__(
        self,
        elements: Tuple[Literal, ...],
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize LiteralTuple."""
        super().__init__(loc)
        self.elements = elements
        self.type_ = TupleType([elem.type_ for elem in elements])
        self.loc = loc


@public
@typechecked
class LiteralSet(Literal):
    """Literal representation of a Set."""

    elements: Set[Literal]

    def __init__(
        self, elements: Set[Literal], loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralSet."""
        super().__init__(loc)
        self.elements = set(elements)
        unique_types = {type(elem.type_) for elem in elements}
        self.type_ = SetType(
            unique_types.pop()() if len(unique_types) == 1 else Int32()
        )
        self.loc = loc


@public
@typechecked
class LiteralDict(Literal):
    """Literal representation of a Dictionary."""

    elements: Dict[Literal, Literal]

    def __init__(
        self,
        elements: Dict[Literal, Literal],
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize LiteralDict."""
        super().__init__(loc)
        self.elements = dict(elements)
        key_types = {type(k.type_) for k in elements.keys()}
        value_types = {type(v.type_) for v in elements.values()}
        self.type_ = DictType(
            key_types.pop()() if len(key_types) == 1 else Int32(),
            value_types.pop()() if len(value_types) == 1 else Int32(),
        )
        self.loc = loc
