"""ASTX literal representations of collection types."""

from __future__ import annotations

from typing import Dict, List, Set, Tuple

from astx.base import AST, NO_SOURCE_LOCATION, SourceLocation
from astx.literals.base import Literal
from astx.tools.typing import typechecked
from astx.types.base import AnyType
from astx.types.collections import ListType, MapType, SetType, TupleType

from public import public

@public
@typechecked
class LiteralList(Literal):
    """Literal representation of a list."""

    elements: List[Literal]

    def __init__(
        self, elements: List[Literal], loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        super().__init__(loc)
        self.elements = elements
        element_types = {elem.type_ for elem in elements}

        if len(element_types) == 1:
            element_type: AST = element_types.pop()
        else:
            element_type = AnyType()

        self.type_ = ListType(element_type)
        self.loc = loc

    def __str__(self) -> str:
        return f"LiteralList({self.elements})"

    def __repr__(self) -> str:
        return self.__str__()


@public
@typechecked
class LiteralSet(Literal):
    """Literal representation of a set."""

    elements: Set[Literal]

    def __init__(
        self, elements: Set[Literal], loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        super().__init__(loc)
        self.elements = elements
        element_types = {elem.type_ for elem in elements}

        if len(element_types) == 1:
            element_type: AST = element_types.pop()
        else:
            element_type = AnyType()

        self.type_ = SetType(element_type)
        self.loc = loc

    def __str__(self) -> str:
        return f"LiteralSet({self.elements})"

    def __repr__(self) -> str:
        return self.__str__()


@public
@typechecked
class LiteralMap(Literal):
    """Literal representation of a map/dictionary."""

    elements: Dict[Literal, Literal]

    def __init__(
        self,
        elements: Dict[Literal, Literal],
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        super().__init__(loc)
        self.elements = elements
        key_types = {key.type_ for key in elements}
        value_types = {value.type_ for value in elements.values()}

        if len(key_types) == 1:
            key_type: AST = key_types.pop()
        else:
            key_type = AnyType()

        if len(value_types) == 1:
            value_type: AST = value_types.pop()
        else:
            value_type = AnyType()

        self.type_ = MapType(key_type, value_type)
        self.loc = loc

    def __str__(self) -> str:
        return f"LiteralMap({self.elements})"

    def __repr__(self) -> str:
        return self.__str__()


@public
@typechecked
class LiteralTuple(Literal):
    """Literal representation of a tuple."""

    elements: Tuple[Literal, ...]

    def __init__(
        self,
        elements: Tuple[Literal, ...],
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        super().__init__(loc)
        self.elements = elements
        element_types: List[AST] = [elem.type_ for elem in elements]
        self.type_ = TupleType(element_types)
        self.loc = loc

    def __str__(self) -> str:
        return f"LiteralTuple({self.elements})"

    def __repr__(self) -> str:
        return self.__str__()
