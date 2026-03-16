"""
title: ASTx Data Types module.
"""

from __future__ import annotations

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ReprStruct,
    SourceLocation,
)
from astx.literals.base import Literal
from astx.tools.typing import typechecked
from astx.types.numeric import (
    Complex,
    Complex32,
    Complex64,
    Float16,
    Float32,
    Float64,
    Int8,
    Int16,
    Int32,
    Int64,
    Int128,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
    UInt128,
)


@public
@typechecked
class LiteralInt8(Literal):
    """
    title: LiteralInt8 data type class.
    attributes:
      type_:
        type: Int8
      loc:
        type: SourceLocation
      value:
        type: int
    """

    type_: Int8
    loc: SourceLocation

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralInt8.
        parameters:
          value:
            type: int
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = Int8()
        self.loc = loc


@public
@typechecked
class LiteralInt16(Literal):
    """
    title: LiteralInt16 data type class.
    attributes:
      type_:
        type: Int16
      loc:
        type: SourceLocation
      value:
        type: int
    """

    type_: Int16
    loc: SourceLocation

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralInt16.
        parameters:
          value:
            type: int
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = Int16()
        self.loc = loc


@public
@typechecked
class LiteralInt32(Literal):
    """
    title: LiteralInt32 data type class.
    attributes:
      type_:
        type: Int32
      loc:
        type: SourceLocation
      value:
        type: int
    """

    type_: Int32
    loc: SourceLocation

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralInt32.
        parameters:
          value:
            type: int
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = Int32()
        self.loc = loc


@public
@typechecked
class LiteralInt64(Literal):
    """
    title: LiteralInt64 data type class.
    attributes:
      type_:
        type: Int64
      loc:
        type: SourceLocation
      value:
        type: int
    """

    type_: Int64
    loc: SourceLocation

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralInt64.
        parameters:
          value:
            type: int
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = Int64()
        self.loc = loc


@public
@typechecked
class LiteralInt128(Literal):
    """
    title: LiteralInt128 data type class.
    attributes:
      type_:
        type: Int128
      loc:
        type: SourceLocation
      value:
        type: int
    """

    type_: Int128
    loc: SourceLocation

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralInt128.
        parameters:
          value:
            type: int
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = Int128()
        self.loc = loc


@public
@typechecked
class LiteralUInt8(Literal):
    """
    title: LiteralUInt8 data type class.
    attributes:
      type_:
        type: UInt8
      loc:
        type: SourceLocation
      value:
        type: int
    """

    type_: UInt8
    loc: SourceLocation

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralUInt8.
        parameters:
          value:
            type: int
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = UInt8()
        self.loc = loc


@public
@typechecked
class LiteralUInt16(Literal):
    """
    title: LiteralUInt16 data type class.
    attributes:
      type_:
        type: UInt16
      loc:
        type: SourceLocation
      value:
        type: int
    """

    type_: UInt16
    loc: SourceLocation

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralUInt16.
        parameters:
          value:
            type: int
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = UInt16()
        self.loc = loc


@public
@typechecked
class LiteralUInt32(Literal):
    """
    title: LiteralUInt32 data type class.
    attributes:
      type_:
        type: UInt32
      loc:
        type: SourceLocation
      value:
        type: int
    """

    type_: UInt32
    loc: SourceLocation

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralUInt32.
        parameters:
          value:
            type: int
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = UInt32()
        self.loc = loc


@public
@typechecked
class LiteralUInt64(Literal):
    """
    title: LiteralUInt64 data type class.
    attributes:
      type_:
        type: UInt64
      loc:
        type: SourceLocation
      value:
        type: int
    """

    type_: UInt64
    loc: SourceLocation

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralUInt64.
        parameters:
          value:
            type: int
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = UInt64()
        self.loc = loc


@public
@typechecked
class LiteralUInt128(Literal):
    """
    title: LiteralUInt128 data type class.
    attributes:
      type_:
        type: UInt128
      loc:
        type: SourceLocation
      value:
        type: int
    """

    type_: UInt128
    loc: SourceLocation

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralUInt128.
        parameters:
          value:
            type: int
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = UInt128()
        self.loc = loc


@public
@typechecked
class LiteralFloat16(Literal):
    """
    title: LiteralFloat16 data type class.
    attributes:
      type_:
        type: Float16
      loc:
        type: SourceLocation
      value:
        type: float
    """

    type_: Float16
    loc: SourceLocation

    value: float

    def __init__(
        self, value: float, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralFloat16.
        parameters:
          value:
            type: float
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = Float16()
        self.loc = loc


@public
@typechecked
class LiteralFloat32(Literal):
    """
    title: LiteralFloat32 data type class.
    attributes:
      type_:
        type: Float32
      loc:
        type: SourceLocation
      value:
        type: float
    """

    type_: Float32
    loc: SourceLocation

    value: float

    def __init__(
        self, value: float, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralFloat32.
        parameters:
          value:
            type: float
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = Float32()
        self.loc = loc


@public
@typechecked
class LiteralFloat64(Literal):
    """
    title: LiteralFloat64 data type class.
    attributes:
      type_:
        type: Float64
      loc:
        type: SourceLocation
      value:
        type: float
    """

    type_: Float64
    loc: SourceLocation

    value: float

    def __init__(
        self, value: float, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """
        title: Initialize LiteralFloat64.
        parameters:
          value:
            type: float
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = value
        self.type_ = Float64()
        self.loc = loc


@public
@typechecked
class LiteralComplex(Literal):
    """
    title: Base class for literal complex numbers.
    attributes:
      type_:
        type: Complex
      value:
        type: tuple[float, float]
    """

    type_: Complex
    value: tuple[float, float]

    def __init__(
        self,
        real: float,
        imag: float,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """
        title: Initialize a generic complex number.
        parameters:
          real:
            type: float
          imag:
            type: float
          loc:
            type: SourceLocation
        """
        super().__init__(loc)
        self.value = real, imag

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        return f"LiteralComplex({self.value[0]} + {self.value[1]}j)"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST representation for the complex literal.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = f"{self.__class__.__name__}: {self.value}"
        value: ReprStruct = {
            "real": self.value[0],
            "imag": self.value[1],
        }
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class LiteralComplex32(LiteralComplex):
    """
    title: LiteralComplex32 data type class.
    attributes:
      value:
        type: tuple[float, float]
      type_:
        type: Complex32
    """

    type_: Complex32

    def __init__(
        self,
        real: float,
        imag: float,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """
        title: Initialize LiteralComplex32.
        parameters:
          real:
            type: float
          imag:
            type: float
          loc:
            type: SourceLocation
        """
        super().__init__(real, imag, loc)
        self.type_ = Complex32()


@public
@typechecked
class LiteralComplex64(LiteralComplex):
    """
    title: LiteralComplex64 data type class.
    attributes:
      value:
        type: tuple[float, float]
      type_:
        type: Complex64
    """

    type_: Complex64

    def __init__(
        self,
        real: float,
        imag: float,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """
        title: Initialize LiteralComplex64.
        parameters:
          real:
            type: float
          imag:
            type: float
          loc:
            type: SourceLocation
        """
        super().__init__(real, imag, loc)
        self.type_ = Complex64()
