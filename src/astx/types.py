"""AST types module."""

from __future__ import annotations

from typing import Dict, List, Union

try:
    from typing_extensions import TypeAlias
except ImportError:
    from typing import TypeAlias  # type: ignore[no-redef,attr-defined]


PrimitivesStruct: TypeAlias = Union[int, str, float, bool]
DataTypesStruct: TypeAlias = Union[
    PrimitivesStruct, Dict[str, "DataTypesStruct"], List["DataTypesStruct"]
]
DictDataTypesStruct: TypeAlias = Dict[str, DataTypesStruct]
ReprStruct: TypeAlias = Union[List[DataTypesStruct], DictDataTypesStruct]
