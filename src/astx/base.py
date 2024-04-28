"""AST classes and functions."""

from __future__ import annotations

import json

from abc import abstractmethod
from enum import Enum
from typing import ClassVar, Dict, List, Optional, Type, Union, cast

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


def is_using_jupyter_notebook() -> bool:
    """Check if it is executed in a jupyter notebook."""
    try:
        from IPython import get_ipython  # type: ignore

        if "IPKernelApp" in get_ipython().config:  # type: ignore
            return True
    except Exception:
        pass
    return False


@public
class SourceLocation:
    line: int
    col: int

    def __init__(self, line: int, col: int):
        self.line = line
        self.col = col

    def __str__(self) -> str:
        return "{" + f"line: {self.line}, col: {self.col}" + "}"

    def __repr__(self) -> str:
        return str(self)


NO_SOURCE_LOCATION = SourceLocation(-1, -1)


@public
class ASTKind(Enum):
    """The expression kind class used for downcasting."""

    GenericKind = -100
    ModuleKind = -101

    # variables
    ArgumentKind = -200
    VariableKind = -201
    VarDeclKind = -202
    VarsDeclKind = -203
    VariableAssignmentKind = -204
    VarsAssignKind = -205

    # operators
    UnaryOpKind = -300
    BinaryOpKind = -301

    # functions
    PrototypeKind = -400
    FunctionKind = -401
    CallKind = -402
    ReturnKind = -403

    # control flow
    IfKind = -500
    ForKind = -501

    # data types
    NullDTKind = -600
    BooleanDTKind = -601
    Int8DTKind = -602
    UInt8DTKind = -603
    Int16DTKind = -604
    UInt16DTKind = -605
    Int32DTKind = -606
    UInt32DTKind = -607
    Int64DTKind = -608
    UInt64DTKind = -609
    FloatDTKind = -610
    DoubleDTKind = -611
    BinaryDTKind = -612
    StringDTKind = -613
    FixedSizeBinaryDTKind = -614
    Date32DTKind = -615
    Date64DTKind = -616
    TimestampDTKind = -617
    Time32DTKind = -618
    Time64DTKind = -619
    Decimal128DTKind = -620
    Decimal256DTKind = -621


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
    parent: Optional[ASTNodes] = None
    ref: str

    def __init__(
        self,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the AST instance."""
        self.kind = ASTKind.GenericKind
        self.loc = loc
        self.ref = ""
        self.comment = ""
        self.parent = parent
        self._update_parent()

    def __str__(self) -> str:
        """Return an string that represents the object."""
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        """Return an string that represents the object."""
        if not is_using_jupyter_notebook():
            # note: this should be replaced by asciinet approach
            return f"{self.__str__()}"
        return ""

    def _repr_png_(self) -> None:
        """
        Return PNG representation of the Graphviz object.

        This method is specially recognized by Jupyter Notebook to display
        a Graphviz diagram inline.
        """
        # importing it here in order to avoid cyclic import issue
        from astx.viz import visualize

        visualize(self.get_struct(simplified=False))

    def _update_parent(self) -> None:
        """Update the parent node."""
        if self.parent:
            self.parent.nodes.append(self)

    def _get_metadata(self) -> ReprStruct:
        """Return the metadata for the requested AST."""
        metadata = {
            "loc": self.loc,
            "comment": self.comment,
            "ref": self.ref,
            "kind": self.kind,
        }
        return cast(ReprStruct, metadata)

    def _prepare_struct(
        self, key: str, value: Union[str, ReprStruct], simplified: bool
    ) -> ReprStruct:
        if simplified:
            struct = {key: value}
        else:
            struct = {
                key: {
                    "value": value,
                    "metadata": self._get_metadata(),
                }
            }
        return cast(ReprStruct, struct)

    @abstractmethod
    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a structure that represents the node object."""
        ...

    def to_yaml(self, simplified: bool = False) -> str:
        """Return an yaml string that represents the object."""
        return str(
            yaml.dump(self.get_struct(simplified=simplified), sort_keys=False)
        )

    def to_json(self, simplified: bool = False) -> str:
        """Return an json string that represents the object."""
        return json.dumps(self.get_struct(simplified=simplified), indent=2)


@public
class ASTNodes(AST):
    """AST with a list of nodes."""

    nodes: list[AST]


@public
class Expr(AST):
    """AST main expression class."""

    nbytes: int = 0


ExprType: TypeAlias = Type[Expr]


@public
class Undefined(Expr):
    """Undefined expression class."""

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a simple structure that represents the object."""
        value = "UNDEFINED"
        key = "DATA-TYPE"
        return self._prepare_struct(key, value, simplified)


@public
class DataType(Expr):
    """AST main expression class."""

    type_: ExprType
    name: str
    _tmp_id: ClassVar[int] = 0

    def __init__(
        self,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(loc)
        self.name = f"temp_{DataType._tmp_id}"
        DataType._tmp_id += 1
        # set it as a generic data type
        self.type_: ExprType = DataType
        self.parent = parent

    def __str__(self) -> str:
        """Return an string that represents the object."""
        return f"{self.__class__.__name__}: {self.name}"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a simple structure that represents the object."""
        key = "DATA-TYPE"
        value = self.name
        return self._prepare_struct(key, value, simplified)


@public
class OperatorType(DataType):
    """AST main expression class."""


@public
class StatementType(AST):
    """AST main expression class."""
