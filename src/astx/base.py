"""AST classes and functions."""

from __future__ import annotations

import json

from abc import abstractmethod
from enum import Enum
from hashlib import sha256
from typing import ClassVar, Optional, Type, Union, cast

from astx.types import ReprStruct
from astx.viz import graph_to_ascii, traverse_ast_ascii

try:
    from typing_extensions import TypeAlias
except ImportError:
    from typing import TypeAlias  # type: ignore[no-redef,attr-defined]


try:
    from typing_extensions import Self
except ImportError:
    from typing import Self  # type: ignore[no-redef,attr-defined]


import yaml

from public import public

__all__ = ["ExprType"]


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
    ArgumentsKind = -201
    VariableKind = -202
    VarDeclKind = -203
    VarsDeclKind = -204
    VariableAssignmentKind = -205
    VarsAssignKind = -206

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
    ForCountKind = -501
    ForRangeKind = -502
    WhileKind = -503

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

    def __hash__(self) -> int:
        value = sha256(f"{self.get_struct()}".encode("utf8")).digest()
        return int.from_bytes(value, "big")

    def __str__(self) -> str:
        """Return an string that represents the object."""
        return f"{self.__class__.__name__}"

    def __repr__(self) -> str:
        """Return an string that represents the object."""
        if not is_using_jupyter_notebook():
            graph = traverse_ast_ascii(self.get_struct(simplified=True))
            return graph_to_ascii(graph)
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
        if self.parent is not None:
            self.parent.append(self)

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
                    "content": value,
                    "metadata": self._get_metadata(),
                }
            }
        return cast(ReprStruct, struct)

    @abstractmethod
    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a structure that represents the node object."""

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

    name: str
    nodes: list[AST]
    position: int = 0

    def __init__(
        self,
        name: str = "entry",
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the AST instance."""
        super().__init__(loc=loc, parent=parent)
        self.name = name
        # note: maybe it would be nice to add options for rules, so
        #       it could have specific rules for the type of AST
        #       accepted
        self.nodes: list[AST] = []
        self.position: int = 0

    def __iter__(self) -> Self:
        """Overload `iter` magic function."""
        return self

    def __next__(self) -> AST:
        """Overload `next` magic function."""
        if self.position >= len(self.nodes):
            self.position = 0
            raise StopIteration()

        i = self.position
        self.position += 1
        return self.nodes[i]

    def append(self, value: AST) -> None:
        """Append a new node to the stack."""
        self.nodes.append(value)

    def __getitem__(self, index: int) -> AST:
        """Support subscripting to get nodes by index."""
        return self.nodes[index]

    def __len__(self) -> int:
        """Return the number of nodes, supports len function."""
        return len(self.nodes)


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
