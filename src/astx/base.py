"""AST classes and functions."""

from __future__ import annotations

import json

from abc import abstractmethod
from enum import Enum
from hashlib import sha256
from typing import (
    ClassVar,
    Dict,
    Generic,
    Iterator,
    List,
    Optional,
    Union,
    cast,
)

from astx.tools.typing import typechecked

try:
    from typing_extensions import TypeAlias
except ImportError:
    from typing import TypeAlias  # type: ignore[no-redef,attr-defined]


try:
    from typing_extensions import TypeVar
except ImportError:
    from typing import TypeVar  # type: ignore[assignment]


import yaml

from public import public

ASTType = TypeVar("ASTType", bound="AST", default="AST")


__all__ = [
    "DataTypesStruct",
    "DictDataTypesStruct",
    "ExprType",
    "PrimitivesStruct",
    "ReprStruct",
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
@typechecked
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
@typechecked
class ASTKind(Enum):
    """The expression kind class used for downcasting."""

    GenericKind = -100
    ModuleKind = -101
    ParenthesizedExprKind = -102

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
    WalrusOpKind = -302
    AssignmentExprKind = -303
    AugmentedAssignKind = -304

    # functions
    PrototypeKind = -400
    FunctionDefKind = -401
    CallKind = -402
    ReturnKind = -403
    LambdaExprKind = -404
    FunctionAsyncDefKind = -405
    AwaitExprKind = -406
    YieldExprKind = -510
    YieldFromExprKind = -407

    # control flow
    IfStmtKind = -500
    ForCountLoopStmtKind = -501
    ForRangeLoopStmtKind = -502
    WhileStmtKind = -503
    ForRangeLoopExprKind = -504
    ForCountLoopExprKind = -505
    WhileExprKind = -506
    IfExprKind = -507
    CaseStmtKind = -508
    SwitchStmtKind = -509
    GotoStmtKind = -511
    WithStmtKind = -512
    AsyncRangeLoopStmtKind = -513
    AsyncRangeLoopExprKind = -514

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
    UTF8CharDTKind = -622
    UTF8StringDTKind = -623
    TimeDTKind = -624
    DateDTKind = -625
    DateTimeDTKind = -626

    # imports(packages)
    ImportStmtKind = -700
    ImportFromStmtKind = -701
    AliasExprKind = -702
    ImportExprKind = -800
    ImportFromExprKind = -801

    TypeCastExprKind = -809

    # classes
    ClassDefStmtKind = -900
    ClassDeclStmtKind = -901
    EnumDeclStmtKind = -902
    StructDeclStmtKind = -903
    StructDefStmtKind = -904

    # subscrpts
    SubscriptExprKind = -1000

    # exceptions
    ThrowStmtKind = -1100
    CatchHandlerStmtKind = -1101
    ExceptionHandlerStmtKind = -1102
    FinallyHandlerStmtKind = -1103

    # boolops
    AndOpKind = -1200
    OrOpKind = -1201
    XorOpKind = -1202
    NandOpKind = -1203
    NorOpKind = -1204
    XnorOpKind = -1205
    NotOpKind = -1206


class ASTMeta(type):
    def __str__(cls) -> str:
        """Return an string that represents the object."""
        return cls.__name__


@public
@typechecked
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
            from astx.viz import graph_to_ascii, traverse_ast_ascii

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
            "loc": {"line": self.loc.line, "col": self.loc.col},
            "comment": self.comment,
            "ref": self.ref,
            "kind": self.kind.value,
        }
        return cast(ReprStruct, metadata)

    def _prepare_struct(
        self,
        key: str,
        value: Union[PrimitivesStruct, ReprStruct],
        simplified: bool,
    ) -> ReprStruct:
        struct: ReprStruct = (
            {
                key: {
                    "content": value,
                    "metadata": self._get_metadata(),
                }
            }
            if not simplified
            else {key: value}
        )
        return struct

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
@typechecked
class ASTNodes(Generic[ASTType], AST):
    """AST with a list of nodes, supporting type-specific elements."""

    name: str
    nodes: list[ASTType]
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
        self.nodes: list[ASTType] = []
        self.position: int = 0

    def __iter__(self) -> Iterator[ASTType]:
        """Overload `iter` magic function."""
        self.position = 0  # Reset position for fresh iteration
        return self

    def __next__(self) -> ASTType:
        """Overload `next` magic function."""
        if self.position >= len(self.nodes):
            self.position = 0
            raise StopIteration()

        i = self.position
        self.position += 1
        return self.nodes[i]

    def append(self, value: ASTType) -> None:
        """Append a new node to the stack."""
        self.nodes.append(value)

    def __getitem__(self, index: int) -> ASTType:
        """Support subscripting to get nodes by index."""
        return self.nodes[index]

    def __len__(self) -> int:
        """Return the number of nodes, supports len function."""
        return len(self.nodes)

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a string that represents the object."""
        args_nodes = []

        for node in self.nodes:
            args_nodes.append(node.get_struct(simplified))

        key = str(self)
        value = cast(ReprStruct, args_nodes)
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class Expr(AST):
    """AST main expression class."""

    nbytes: int = 0


@public
@typechecked
class Identifier(Expr):
    """AST class for identifiers."""

    value: str

    def __init__(
        self,
        value: str,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the Identifier instance."""
        super().__init__(loc=loc, parent=parent)
        self.value = value

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a structure that represents the Identifier object."""
        key = f"IDENTIFIER[{self.value}]"
        return self._prepare_struct(key, self.value, simplified)


@public
@typechecked
class ExprType(Expr):
    """ExprType expression class."""

    nbytes: int = 0

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a structure that represents the node object."""
        return {"Type": self.__class__.__name__}


@public
@typechecked
class Undefined(Expr):
    """Undefined expression class."""

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a simple structure that represents the object."""
        value = "UNDEFINED"
        key = "UNDEFINED"
        return self._prepare_struct(key, value, simplified)


PrimitivesStruct: TypeAlias = Union[
    int,
    str,
    float,
    bool,
    Undefined,
]
DataTypesStruct: TypeAlias = Union[
    PrimitivesStruct, Dict[str, "DataTypesStruct"], List["DataTypesStruct"]
]
DictDataTypesStruct: TypeAlias = Dict[str, DataTypesStruct]
ReprStruct: TypeAlias = Union[
    List[DataTypesStruct],
    DictDataTypesStruct,
    Undefined,
]


@public
@typechecked
class DataType(ExprType):
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
        self.type_: ExprType = ExprType()
        self.parent = parent

    def __str__(self) -> str:
        """Return an string that represents the object."""
        return f"{self.__class__.__name__}: {self.name}"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return a simple structure that represents the object."""
        key = f"DATA-TYPE[{self.__class__.__name__}]"
        value = self.name
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class OperatorType(DataType):
    """AST main expression class."""


@public
@typechecked
class StatementType(AST):
    """AST main expression class."""


@public
@typechecked
class ParenthesizedExpr(DataType):
    """AST class for explicitly grouped expressions (parentheses retained)."""

    value: Expr

    def __init__(
        self,
        value: Expr,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """Initialize the ParenthesizedExpr instance."""
        super().__init__(loc=loc, parent=parent)
        self.type_ = getattr(value, "type_", DataType())
        self.value = value
        self.kind = ASTKind.ParenthesizedExprKind

    def __str__(self) -> str:
        """Return a string representation of the object with parentheses."""
        return f"ParenthesizedExpr({self.value})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """Return the AST structure of the object."""
        key = "PARENTHESIZED-EXPR"
        value = self.value.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)
