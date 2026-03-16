"""
title: ASTx Collection Data Types.
"""

from __future__ import annotations

from public import public

from astx.base import ExprType
from astx.tools.typing import typechecked
from astx.types.base import AnyType


@public
@typechecked
class CollectionType(AnyType):
    """
    title: Base class for collection data types.
    """


@public
@typechecked
class ListType(CollectionType):
    """
    title: List data type expression.
    attributes:
      element_types:
        type: list[ExprType]
    """

    element_types: list[ExprType]

    def __init__(self, element_types: list[ExprType]) -> None:
        """
        title: Initialize ListType with an element type.
        parameters:
          element_types:
            type: list[ExprType]
        """
        self.element_types = element_types

    def __str__(self) -> str:
        """
        title: Return string representation of ListType.
        returns:
          type: str
        """
        types_str = ", ".join(str(t) for t in self.element_types)
        return f"ListType[{types_str}]"


@public
@typechecked
class SetType(CollectionType):
    """
    title: Set data type expression.
    attributes:
      element_type:
        type: ExprType
    """

    element_type: ExprType

    def __init__(self, element_type: ExprType) -> None:
        """
        title: Initialize SetType with an element type.
        parameters:
          element_type:
            type: ExprType
        """
        self.element_type = element_type

    def __str__(self) -> str:
        """
        title: Return string representation of SetType.
        returns:
          type: str
        """
        return f"SetType[{self.element_type}]"


@public
@typechecked
class DictType(CollectionType):
    """
    title: Dictionary data type expression.
    attributes:
      key_type:
        type: ExprType
      value_type:
        type: ExprType
    """

    key_type: ExprType
    value_type: ExprType

    def __init__(self, key_type: ExprType, value_type: ExprType) -> None:
        """
        title: Initialize DictType with key-value types.
        parameters:
          key_type:
            type: ExprType
          value_type:
            type: ExprType
        """
        self.key_type = key_type
        self.value_type = value_type

    def __str__(self) -> str:
        """
        title: Return string representation of DictType.
        returns:
          type: str
        """
        return f"DictType[{self.key_type}, {self.value_type}]"


@public
@typechecked
class TupleType(CollectionType):
    """
    title: Tuple data type expression.
    attributes:
      element_types:
        type: list[ExprType]
    """

    element_types: list[ExprType]

    def __init__(self, element_types: list[ExprType]) -> None:
        """
        title: Initialize TupleType with multiple element types.
        parameters:
          element_types:
            type: list[ExprType]
        """
        self.element_types = element_types

    def __str__(self) -> str:
        """
        title: Return string representation of TupleType.
        returns:
          type: str
        """
        types_str = ", ".join(str(t) for t in self.element_types)
        return f"TupleType[{types_str}]"
