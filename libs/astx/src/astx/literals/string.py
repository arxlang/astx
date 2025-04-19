"""ASTx Data Types module for strings."""

from __future__ import annotations

from typing import Any, Dict, List, Optional

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    Expr,
    Identifier,
    ReprStruct,
    SourceLocation,
)
from astx.literals.base import Literal
from astx.tools.typing import typechecked
from astx.types.string import String, UTF8Char, UTF8String
from astx.variables import Variable


@public
@typechecked
class LiteralString(Literal):
    """LiteralString data type class."""

    value: str

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        """Initialize LiteralString."""
        super().__init__(loc)
        self.value = value
        self.type_ = String()
        self.loc = loc

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"LiteralString({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = f"LiteralString: {self.value}"
        value = self.value
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class LiteralUTF8String(LiteralString):
    """Literal class for UTF-8 strings."""

    value: str

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        super().__init__(value=value, loc=loc)
        self.type_ = UTF8String()

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"LiteralUTF8String({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the structure of the object in a simplified."""
        key = f"LiteralUTF8String: {self.value}"
        value = self.value
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class LiteralUTF8Char(LiteralString):
    """Literal class for UTF-8 characters."""

    value: str

    def __init__(
        self, value: str, loc: SourceLocation = NO_SOURCE_LOCATION
    ) -> None:
        super().__init__(value=value, loc=loc)
        self.type_ = UTF8Char()

    def __str__(self) -> str:
        """Return a string representation of the object."""
        return f"LiteralUTF8Char({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the structure of the object in a simplified."""
        key = f"LiteralUTF8Char: {self.value}"
        value = self.value
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class FormattedValue(Expr):
    """Represents formatted value parts within a JoinedStr (e.g., {x:.2f})."""

    value: Expr
    conversion: Optional[int]
    format_spec: Optional[Expr]

    kind: ASTKind = ASTKind.FormattedValueKind

    def __init__(
        self,
        value: Expr,
        conversion: Optional[int] = None,
        format_spec: Optional[Expr] = None,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(loc=loc, parent=parent)
        self.value = value
        self.conversion = conversion
        self.format_spec = format_spec

    def __str__(self) -> str:
        """Return a string representation of the formatted value part."""
        if isinstance(self.value, Variable):
            value_str = self.value.name
        elif isinstance(self.value, Identifier):
            value_str = self.value.value
        elif isinstance(self.value, LiteralString):
            value_str = repr(self.value.value)
        elif isinstance(self.value, Literal):
            value_str = str(self.value.value)
        else:
            value_str = str(self.value)

        conv_char = f"!{chr(self.conversion)}" if self.conversion else ""

        fmt_spec_inner_str = ""
        if isinstance(self.format_spec, LiteralString):
            fmt_spec_inner_str = self.format_spec.value
        elif self.format_spec is not None:
            fmt_spec_inner_str = str(self.format_spec)

        fmt_spec_str = f":{fmt_spec_inner_str}" if self.format_spec else ""

        return f"FormattedValue({value_str}{conv_char}{fmt_spec_str})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        content: Dict[str, Any] = {"value": self.value.get_struct(simplified)}
        if self.conversion is not None:
            content["conversion"] = chr(self.conversion)
        if self.format_spec is not None:
            content["format_spec"] = self.format_spec.get_struct(simplified)

        key = "FormattedValue"
        return self._prepare_struct(key, content, simplified)


@public
@typechecked
class JoinedStr(Expr):
    """Represents an f-string literal (e.g., f'hello {name}')."""

    values: List[Expr]

    kind: ASTKind = ASTKind.JoinedStrKind

    def __init__(
        self,
        values: List[Expr],
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(loc=loc, parent=parent)
        for val in values:
            if not isinstance(val, (LiteralString, FormattedValue)):
                raise TypeError(
                    "JoinedStr values must be LiteralString or FormattedValue"
                )
        self.values = values

    def __str__(self) -> str:
        """Return a string representation of the joined string structure."""
        value_strs = [str(v) for v in self.values]
        return f"JoinedStr([{', '.join(value_strs)}])"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        content: Dict[str, Any] = {
            "values": [v.get_struct(simplified) for v in self.values]
        }
        key = "JoinedStr"
        return self._prepare_struct(key, content, simplified)
