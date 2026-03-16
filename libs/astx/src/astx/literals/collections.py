"""
title: ASTx Collection Literals.
"""

from __future__ import annotations

from public import public

from astx.base import NO_SOURCE_LOCATION, SourceLocation
from astx.literals.base import Literal
from astx.tools.typing import typechecked
from astx.types.collections import DictType, ListType, SetType, TupleType
from astx.types.numeric import Int32


@public
@typechecked
class LiteralList(Literal):
    """
    title: Literal representation of a List.
    attributes:
      type_:
        type: ListType
      loc:
        type: SourceLocation
      elements:
        type: list[Literal]
    """

    type_: ListType
    loc: SourceLocation

    elements: list[Literal]

    def __init__(
        self, elements: list[Literal], loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralList.
        parameters:
          elements:
            type: list[Literal]
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.elements = list(elements)  # Ensure correct type
        unique_types = {type(elem.type_) for elem in elements}
        self.type_ = ListType([t() for t in unique_types])
        self.loc = loc


@public
@typechecked
class LiteralTuple(Literal):
    """
    title: Literal representation of a Tuple.
    attributes:
      type_:
        type: TupleType
      loc:
        type: SourceLocation
      elements:
        type: tuple[Literal, Ellipsis]
    """

    type_: TupleType
    loc: SourceLocation

    elements: tuple[Literal, ...]

    def __init__(
        self,
        elements: tuple[Literal, ...],
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """
        title: Initialize LiteralTuple.
        parameters:
          elements:
            type: tuple[Literal, Ellipsis]
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.elements = elements
        self.type_ = TupleType([elem.type_ for elem in elements])
        self.loc = loc


@public
@typechecked
class LiteralSet(Literal):
    """
    title: Literal representation of a Set.
    attributes:
      type_:
        type: SetType
      loc:
        type: SourceLocation
      elements:
        type: set[Literal]
    """

    type_: SetType
    loc: SourceLocation

    elements: set[Literal]

    def __init__(
        self, elements: set[Literal], loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralSet.
        parameters:
          elements:
            type: set[Literal]
          loc:
            type: SourceLocation
        """
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
    """
    title: Literal representation of a Dictionary.
    attributes:
      type_:
        type: DictType
      loc:
        type: SourceLocation
      elements:
        type: dict[Literal, Literal]
    """

    type_: DictType
    loc: SourceLocation

    elements: dict[Literal, Literal]

    def __init__(
        self,
        elements: dict[Literal, Literal],
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """
        title: Initialize LiteralDict.
        parameters:
          elements:
            type: dict[Literal, Literal]
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.elements = dict(elements)
        key_types = {type(k.type_) for k in elements.keys()}
        value_types = {type(v.type_) for v in elements.values()}
        self.type_ = DictType(
            key_types.pop()() if len(key_types) == 1 else Int32(),
            value_types.pop()() if len(value_types) == 1 else Int32(),
        )
        self.loc = loc
