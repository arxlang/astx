"""AST classes and functions."""
from __future__ import annotations

import json

from abc import abstractmethod
from enum import Enum
from typing import ClassVar, Dict, List, Type, Union, cast

try:
    from typing_extensions import TypeAlias
except ImportError:
    from typing import TypeAlias  # type: ignore[no-redef,attr-defined]

import yaml

from public import public

__all__ = ["ExprType"]

PrimitivesStruct: TypeAlias = Union[int, str, float, bool]
DataTypesStruct: TypeAlias = Union[
    PrimitivesStruct, Dict[str, "DataTypesStruct"], List["DataTypesStruct"]
]
ReprStruct: TypeAlias = Union[
    List[DataTypesStruct], Dict[str, DataTypesStruct]
]


@public
class SourceLocation:
    line: int
    col: int

    def __init__(self, line: int, col: int):
        self.line = line
        self.col = col


@public
class ASTKind(Enum):
    """The expression kind class used for downcasting."""

    GenericKind = -1
    ModuleKind = -2

    # variables
    VariableKind = -10
    VarKind = -11  # var keyword for variable declaration

    # operators
    UnaryOpKind = -20
    BinaryOpKind = -21

    # functions
    PrototypeKind = -30
    FunctionKind = -31
    CallKind = -32
    ReturnKind = -33

    # control flow
    IfKind = -40
    ForKind = -41

    # data types
    NullDTKind = -100
    BooleanDTKind = -101
    Int8DTKind = -102
    UInt8DTKind = -103
    Int16DTKind = -104
    UInt16DTKind = -105
    Int32DTKind = -106
    UInt32DTKind = -107
    Int64DTKind = -108
    UInt64DTKind = -109
    FloatDTKind = -110
    DoubleDTKind = -111
    BinaryDTKind = -112
    StringDTKind = -113
    FixedSizeBinaryDTKind = -114
    Date32DTKind = -115
    Date64DTKind = -116
    TimestampDTKind = -117
    Time32DTKind = -118
    Time64DTKind = -119
    Decimal128DTKind = -120
    Decimal256DTKind = -121


class ASTMeta(type):
    def __str__(cls) -> str:
        """Return an string that represents the object."""
        return cls.__name__


@public
class AST(metaclass=ASTMeta):
    """AST main expression class."""

    loc: SourceLocation
    kind: ASTKind
    comment: str
    ref: str

    def __init__(self, loc: SourceLocation = SourceLocation(0, 0)) -> None:
        """Initialize the AST instance."""
        self.kind = ASTKind.GenericKind
        self.loc = loc
        self.ref = ""
        self.comment = ""

    def __str__(self) -> str:
        """Return an string that represents the object."""
        return self.__repr__()

    def __repr__(self) -> str:
        """Return an string that represents the object."""
        return self.__class__.__name__

    def _repr_png_(self) -> None:
        """
        Return PNG representation of the Graphviz object.

        This method is specially recognized by Jupyter Notebook to display
        a Graphviz diagram inline.
        """
        # importing it here in order to avoid cyclic import issue
        from astx.viz import visualize

        data = self.get_struct()
        visualize(data)

    @abstractmethod
    def get_struct(self) -> ReprStruct:
        """Return a simple structure that represents the object."""
        ...

    def to_yaml(self) -> str:
        """Return an yaml string that represents the object."""
        return str(yaml.dump(self.get_struct(), sort_keys=False))

    def to_json(self) -> str:
        """Return an json string that represents the object."""
        return json.dumps(self.get_struct(), indent=2)


@public
class Expr(AST):
    """AST main expression class."""

    nbytes: int = 0


ExprType: TypeAlias = Type[Expr]


@public
class DataType(Expr):
    """AST main expression class."""

    type_: ExprType
    name: str
    _tmp_id: ClassVar[int] = 0

    def __init__(self, loc: SourceLocation = SourceLocation(0, 0)) -> None:
        super().__init__(loc)
        self.name = f"temp_{DataType._tmp_id}"
        DataType._tmp_id += 1
        # set it as a generic data type
        self.type_: ExprType = DataType

    def get_struct(self) -> ReprStruct:
        """Return a simple structure that represents the object."""
        struct = {"DATA-TYPE": self.name}
        return cast(ReprStruct, struct)


@public
class OperatorType(DataType):
    """AST main expression class."""

    def __init__(self) -> None:
        super().__init__()


@public
class StatementType(AST):
    """AST main expression class."""
