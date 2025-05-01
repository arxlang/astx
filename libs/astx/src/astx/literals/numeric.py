"""ASTx Data Types module."""

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
    Floating,
    Int8,
    Int16,
    Int32,
    Int64,
    Int128,
    SignedInteger,
    UInt8,
    UInt16,
    UInt32,
    UInt64,
    UInt128,
    UnsignedInteger,
)


@public
@typechecked
class LiteralInt(Literal):
    """LiteralInteger data type class."""

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralInteger."""
        super().__init__(loc)
        self.value = value
        self.type_ = SignedInteger()
        self.loc = loc


@public
@typechecked
class LiteralInt8(LiteralInt):
    """LiteralInt8 data type class."""

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralInt8."""
        super().__init__(value, loc)
        self.type_ = Int8()


@public
@typechecked
class LiteralInt16(LiteralInt):
    """LiteralInt16 data type class."""

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralInt16."""
        super().__init__(value, loc)
        self.type_ = Int16()


@public
@typechecked
class LiteralInt32(LiteralInt):
    """LiteralInt32 data type class."""

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralInt32."""
        super().__init__(value, loc)
        self.type_ = Int32()


@public
@typechecked
class LiteralInt64(LiteralInt):
    """LiteralInt64 data type class."""

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralInt64."""
        super().__init__(value, loc)
        self.type_ = Int64()


@public
@typechecked
class LiteralInt128(LiteralInt):
    """LiteralInt128 data type class."""

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralInt128."""
        super().__init__(value, loc)
        self.type_ = Int128()


@public
@typechecked
class LiteralUInt(Literal):
    """LiteralUInteger data type class."""

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralUnsignedInteger."""
        super().__init__(loc)
        self.value = value
        self.type_ = UnsignedInteger()
        self.loc = loc


@public
@typechecked
class LiteralUInt8(LiteralUInt):
    """LiteralUInt8 data type class."""

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralUInt8."""
        super().__init__(value, loc)
        self.type_ = UInt8()


@public
@typechecked
class LiteralUInt16(LiteralUInt):
    """LiteralUInt16 data type class."""

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralUInt16."""
        super().__init__(value, loc)
        self.type_ = UInt16()


@public
@typechecked
class LiteralUInt32(LiteralUInt):
    """LiteralUInt32 data type class."""

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralUInt32."""
        super().__init__(value, loc)
        self.type_ = UInt32()


@public
@typechecked
class LiteralUInt64(LiteralUInt):
    """LiteralUInt64 data type class."""

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralUInt64."""
        super().__init__(value, loc)
        self.type_ = UInt64()


@public
@typechecked
class LiteralUInt128(LiteralUInt):
    """LiteralUInt128 data type class."""

    value: int

    def __init__(
        self, value: int, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralUInt128."""
        super().__init__(value, loc)
        self.type_ = UInt128()


@public
@typechecked
class LiteralFloat(Literal):
    """LiteralFloat16 data type class."""

    value: float

    def __init__(
        self, value: float, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralFloat16."""
        super().__init__(loc)
        self.value = value
        self.type_ = Floating()
        self.loc = loc


@public
@typechecked
class LiteralFloat16(LiteralFloat):
    """LiteralFloat16 data type class."""

    value: float

    def __init__(
        self, value: float, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralFloat16."""
        super().__init__(value, loc)
        self.type_ = Float16()


@public
@typechecked
class LiteralFloat32(LiteralFloat):
    """LiteralFloat32 data type class."""

    value: float

    def __init__(
        self, value: float, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralFloat32."""
        super().__init__(value, loc)
        self.type_ = Float32()


@public
@typechecked
class LiteralFloat64(LiteralFloat):
    """LiteralFloat64 data type class."""

    value: float

    def __init__(
        self, value: float, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralFloat64."""
        super().__init__(value, loc)
        self.type_ = Float64()


@public
@typechecked
class LiteralComplex(Literal):
    """Base class for literal complex numbers."""

    type_: Complex
    value: tuple[float, float]

    def __init__(
        self,
        real: float,
        imag: float,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize a generic complex number."""
        super().__init__(loc)
        self.value = real, imag

    def __str__(self) -> str:
        """Return a string that represents the object."""
        return f"LiteralComplex({self.value[0]} + {self.value[1]}j)"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST representation for the complex literal."""
        key = f"{self.__class__.__name__}: {self.value}"
        value: ReprStruct = {
            "real": self.value[0],
            "imag": self.value[1],
        }
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class LiteralComplex32(LiteralComplex):
    """LiteralComplex32 data type class."""

    def __init__(
        self,
        real: float,
        imag: float,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize LiteralComplex32."""
        super().__init__(real, imag, loc)
        self.type_ = Complex32()


@public
@typechecked
class LiteralComplex64(LiteralComplex):
    """LiteralComplex64 data type class."""

    def __init__(
        self,
        real: float,
        imag: float,
        loc: SourceLocation = NO_SOURCE_LOCATION,
    ) -> None:
        """Initialize LiteralComplex64."""
        super().__init__(real, imag, loc)
        self.type_ = Complex64()
