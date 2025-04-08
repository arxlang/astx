"""ASTx Data Types module."""

from __future__ import annotations

from typing import Optional, cast

from public import public

from astx.base import (
    ASTKind,
    ASTNodes,
    NO_SOURCE_LOCATION,
    ReprStruct,
    SourceLocation,
    Expr
)
from astx.literals.base import Literal
from astx.tools.typing import typechecked
from astx.types.string import String
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
class LiteralFormattedString(Literal):
    """Literal class for formatted string expressions (f-strings)."""
    
    value: Expr
    format_spec: Optional[str]
    conversion: Optional[str]

    def __init__(
        self,
        value: Expr,
        format_spec: Optional[str] = None,
        conversion: Optional[str] = None,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize LiteralFormattedString.
        
        Args:
            value: The expression to be formatted within the f-string
            format_spec: Optional format specifier (e.g., '.2f')
            conversion: Optional conversion flag ('s', 'r', 'a')
            loc: Source location information
            parent: Parent node in the AST
        """
        super().__init__(loc=loc, parent=parent)
        self.value = value
        self.format_spec = format_spec
        self.conversion = conversion
        self.type_ = String()
        self.kind = ASTKind.FormattedStringKind

    def __str__(self) -> str:
        """Return a string representation of the object."""
        conversion_str = f"!{self.conversion}" if self.conversion else ""
        format_str = f":{self.format_spec}" if self.format_spec else ""
        return f"LiteralFormattedString({self.value}{conversion_str}{format_str})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        content = {
            "value": self.value.get_struct(simplified),
        }
        
        if self.format_spec:
            content["format_spec"] = self.format_spec
            
        if self.conversion:
            content["conversion"] = self.conversion
            
        key = "LiteralFormattedString"
        return self._prepare_struct(key, cast(ReprStruct, content), simplified)