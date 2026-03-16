"""
title: ASTx Data Types module.
"""

from __future__ import annotations

from typing import Optional

from public import public

from astx.base import (
    NO_SOURCE_LOCATION,
    ASTKind,
    ASTNodes,
    DataType,
    ExprType,
    ReprStruct,
    SourceLocation,
)
from astx.tools.typing import typechecked


@public
@typechecked
class DataTypeOps(DataType):
    """
    title: Overload some magic functions used for the main operations.
    """

    def __hash__(self) -> int:
        """
        title: Ensure that the hash method is not None.
        returns:
          type: int
        """
        return super().__hash__()

    def __add__(self, other: DataType) -> BinaryOp:
        """
        title: Overload the magic `add` method.
        parameters:
          other:
            type: DataType
        returns:
          type: BinaryOp
        """
        return BinaryOp("+", self, other)

    def __eq__(self, other: DataType) -> BinaryOp:  # type: ignore
        """
        title: Overload the magic `eq` method.
        parameters:
          other:
            type: DataType
        returns:
          type: BinaryOp
        """
        return BinaryOp("==", self, other)

    def __floordiv__(self, other: DataType) -> BinaryOp:
        """
        title: Overload the magic `floordiv` method.
        parameters:
          other:
            type: DataType
        returns:
          type: BinaryOp
        """
        return BinaryOp("//", self, other)

    def __ge__(self, other: DataType) -> BinaryOp:
        """
        title: Overload the magic `ge` method.
        parameters:
          other:
            type: DataType
        returns:
          type: BinaryOp
        """
        return BinaryOp(">=", self, other)

    def __gt__(self, other: DataType) -> BinaryOp:
        """
        title: Overload the magic `gt` method.
        parameters:
          other:
            type: DataType
        returns:
          type: BinaryOp
        """
        return BinaryOp(">", self, other)

    def __le__(self, other: DataType) -> BinaryOp:
        """
        title: Overload the magic `le` method.
        parameters:
          other:
            type: DataType
        returns:
          type: BinaryOp
        """
        return BinaryOp("<=", self, other)

    def __lt__(self, other: DataType) -> BinaryOp:
        """
        title: Overload the magic `lt` method.
        parameters:
          other:
            type: DataType
        returns:
          type: BinaryOp
        """
        return BinaryOp("<", self, other)

    def __mod__(self, other: DataType) -> BinaryOp:
        """
        title: Overload the magic `mod` method.
        parameters:
          other:
            type: DataType
        returns:
          type: BinaryOp
        """
        return BinaryOp("%", self, other)

    def __mul__(self, other: DataType) -> BinaryOp:
        """
        title: Overload the magic `mul` method.
        parameters:
          other:
            type: DataType
        returns:
          type: BinaryOp
        """
        return BinaryOp("*", self, other)

    def __ne__(self, other: DataType) -> BinaryOp:  # type: ignore
        """
        title: Overload the magic `ne` method.
        parameters:
          other:
            type: DataType
        returns:
          type: BinaryOp
        """
        return BinaryOp("!=", self, other)

    def __neg__(self) -> UnaryOp:
        """
        title: Overload the magic `neg` method.
        returns:
          type: UnaryOp
        """
        return UnaryOp("-", self)

    def __pos__(self) -> UnaryOp:
        """
        title: Overload the magic `pos` method.
        returns:
          type: UnaryOp
        """
        return UnaryOp("+", self)

    def __pow__(self, other: DataType) -> BinaryOp:
        """
        title: Overload the magic `pow` method.
        parameters:
          other:
            type: DataType
        returns:
          type: BinaryOp
        """
        return BinaryOp("^", self, other)

    def __sub__(self, other: DataType) -> BinaryOp:
        """
        title: Overload the magic `sub` method.
        parameters:
          other:
            type: DataType
        returns:
          type: BinaryOp
        """
        return BinaryOp("-", self, other)

    def __truediv__(self, other: DataType) -> BinaryOp:
        """
        title: Overload the magic `truediv` method.
        parameters:
          other:
            type: DataType
        returns:
          type: BinaryOp
        """
        return BinaryOp("/", self, other)

    def __and__(self, other: DataType) -> AndOp:
        """
        title: Overload the magic 'and' method.
        parameters:
          other:
            type: DataType
        returns:
          type: AndOp
        """
        return AndOp(self, other)

    def __or__(self, other: DataType) -> OrOp:
        """
        title: Overload the magic 'or' method.
        parameters:
          other:
            type: DataType
        returns:
          type: OrOp
        """
        return OrOp(self, other)

    def __xor__(self, other: DataType) -> XorOp:
        """
        title: Overload the magic 'xor' method.
        parameters:
          other:
            type: DataType
        returns:
          type: XorOp
        """
        return XorOp(self, other)

    def __invert__(self) -> NotOp:
        """
        title: Overload the magic 'not' method.
        returns:
          type: NotOp
        """
        return NotOp(self)


@public
@typechecked
class UnaryOp(DataTypeOps):
    """
    title: AST class for the unary operator.
    attributes:
      kind:
        type: ASTKind
      op_code:
        type: str
      operand:
        type: DataType
    """

    kind: ASTKind

    op_code: str
    operand: DataType

    def __init__(
        self,
        op_code: str,
        operand: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Initialize the UnaryOp instance.
        parameters:
          op_code:
            type: str
          operand:
            type: DataType
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(loc=loc, parent=parent)
        self.op_code = op_code
        self.operand = operand
        self.kind = ASTKind.UnaryOpKind

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        return f"UnaryOp[{self.op_code}]({self.operand})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure of the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = f"UNARY[{self.op_code}]"
        value = self.operand.get_struct(simplified)
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class BinaryOp(DataTypeOps):
    """
    title: AST class for the binary operator.
    attributes:
      kind:
        type: ASTKind
      type_:
        type: ExprType
      lhs:
        type: DataType
      rhs:
        type: DataType
      op_code:
        type: str
    """

    kind: ASTKind

    type_: ExprType
    lhs: DataType
    rhs: DataType
    op_code: str

    def __init__(
        self,
        op_code: str,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Initialize the BinaryOp instance.
        parameters:
          op_code:
            type: str
          lhs:
            type: DataType
          rhs:
            type: DataType
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(loc=loc, parent=parent)

        self.op_code = op_code
        self.lhs = lhs
        self.rhs = rhs
        self.kind = ASTKind.BinaryOpKind

        if not (
            isinstance(lhs.type_, DataType) and isinstance(rhs.type_, DataType)
        ):
            raise Exception(
                "For now, binary operators are just allowed for `DataType`."
                f"LHS: {lhs.type_}, RHS: {rhs.type_}"
            )

        if lhs.type_ == rhs.type_:
            self.type_ = lhs.type_
        else:
            # type inference
            self.type_ = max([lhs.type_, rhs.type_], key=lambda v: v.nbytes)

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        return f"BinaryOp[{self.op_code}]({self.lhs},{self.rhs})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure that represents the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = f"BINARY[{self.op_code}]"
        lhs = {"lhs": self.lhs.get_struct(simplified)}
        rhs = {"rhs": self.rhs.get_struct(simplified)}

        content: ReprStruct = {**lhs, **rhs}
        return self._prepare_struct(key, content, simplified)


@public
@typechecked
class BoolBinaryOp(BinaryOp):
    """
    title: Base AST class for boolean binary operations.
    attributes:
      type_:
        type: ExprType
      lhs:
        type: DataType
      rhs:
        type: DataType
      op_code:
        type: str
      kind:
        type: ASTKind
    """

    kind: ASTKind

    def __init__(
        self,
        op_code: str,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(
            op_code=op_code,
            lhs=lhs,
            rhs=rhs,
            loc=loc,
            parent=parent,
        )

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        return f"({self.lhs} {self.op_code} {self.rhs})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure that represents the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = f"BOOL_BINARY_OP[{self.__class__.__name__}]"
        value: ReprStruct = {
            "lhs": self.lhs.get_struct(simplified),
            "rhs": self.rhs.get_struct(simplified),
        }
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class BoolUnaryOp(UnaryOp):
    """
    title: Base AST class for boolean unary operations.
    attributes:
      op_code:
        type: str
      operand:
        type: DataType
      kind:
        type: ASTKind
    """

    kind: ASTKind

    def __init__(
        self,
        op_code: str,
        operand: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        super().__init__(
            op_code=op_code,
            operand=operand,
            loc=loc,
            parent=parent,
        )

    def __str__(self) -> str:
        """
        title: Return a string that represents the object.
        returns:
          type: str
        """
        return f"({self.op_code} {self.operand})"

    def get_struct(self, simplified: bool = False) -> ReprStruct:
        """
        title: Return the AST structure that represents the object.
        parameters:
          simplified:
            type: bool
        returns:
          type: ReprStruct
        """
        key = f"BOOL_UNARY_OP[{self.__class__.__name__}]"
        value: ReprStruct = {"operand": self.operand.get_struct(simplified)}
        return self._prepare_struct(key, value, simplified)


@public
@typechecked
class AndOp(BoolBinaryOp):
    """
    title: AST class for logical AND operation.
    attributes:
      type_:
        type: ExprType
      lhs:
        type: DataType
      rhs:
        type: DataType
      op_code:
        type: str
      kind:
        type: ASTKind
    """

    kind: ASTKind

    kind = ASTKind.AndOpKind
    op_code = "and"

    def __init__(
        self,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Instantiate AST class for logical AND operation.
        parameters:
          lhs:
            type: DataType
          rhs:
            type: DataType
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(
            op_code=self.op_code,
            lhs=lhs,
            rhs=rhs,
            loc=loc,
            parent=parent,
        )


@public
@typechecked
class OrOp(BoolBinaryOp):
    """
    title: AST class for logical OR operation.
    attributes:
      type_:
        type: ExprType
      lhs:
        type: DataType
      rhs:
        type: DataType
      op_code:
        type: str
      kind:
        type: ASTKind
    """

    kind: ASTKind

    kind = ASTKind.OrOpKind
    op_code = "or"

    def __init__(
        self,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Instantiate AST class for logical OR operation.
        parameters:
          lhs:
            type: DataType
          rhs:
            type: DataType
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(
            op_code=self.op_code,
            lhs=lhs,
            rhs=rhs,
            loc=loc,
            parent=parent,
        )


@public
@typechecked
class XorOp(BoolBinaryOp):
    """
    title: AST class for logical XOR operation.
    attributes:
      type_:
        type: ExprType
      lhs:
        type: DataType
      rhs:
        type: DataType
      op_code:
        type: str
      kind:
        type: ASTKind
    """

    kind: ASTKind

    kind = ASTKind.XorOpKind
    op_code = "xor"

    def __init__(
        self,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Instantiate AST class for logical XOR operation.
        parameters:
          lhs:
            type: DataType
          rhs:
            type: DataType
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(
            op_code=self.op_code,
            lhs=lhs,
            rhs=rhs,
            loc=loc,
            parent=parent,
        )


@public
@typechecked
class NandOp(BoolBinaryOp):
    """
    title: AST class for logical NAND operation.
    attributes:
      type_:
        type: ExprType
      lhs:
        type: DataType
      rhs:
        type: DataType
      op_code:
        type: str
      kind:
        type: ASTKind
    """

    kind: ASTKind

    kind = ASTKind.NandOpKind
    op_code = "nand"

    def __init__(
        self,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Instantiate AST class for logical NAND operation.
        parameters:
          lhs:
            type: DataType
          rhs:
            type: DataType
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(
            op_code=self.op_code,
            lhs=lhs,
            rhs=rhs,
            loc=loc,
            parent=parent,
        )


@public
@typechecked
class NorOp(BoolBinaryOp):
    """
    title: AST class for logical NOR operation.
    attributes:
      type_:
        type: ExprType
      lhs:
        type: DataType
      rhs:
        type: DataType
      op_code:
        type: str
      kind:
        type: ASTKind
    """

    kind: ASTKind

    kind = ASTKind.NorOpKind
    op_code = "nor"

    def __init__(
        self,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Instantiate AST class for logical NOR operation.
        parameters:
          lhs:
            type: DataType
          rhs:
            type: DataType
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(
            op_code=self.op_code,
            lhs=lhs,
            rhs=rhs,
            loc=loc,
            parent=parent,
        )


@public
@typechecked
class XnorOp(BoolBinaryOp):
    """
    title: AST class for logical XNOR operation.
    attributes:
      type_:
        type: ExprType
      lhs:
        type: DataType
      rhs:
        type: DataType
      op_code:
        type: str
      kind:
        type: ASTKind
    """

    kind: ASTKind

    kind = ASTKind.XnorOpKind
    op_code = "xnor"

    def __init__(
        self,
        lhs: DataType,
        rhs: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Instantiate AST class for logical XNOR operation.
        parameters:
          lhs:
            type: DataType
          rhs:
            type: DataType
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(
            op_code=self.op_code,
            lhs=lhs,
            rhs=rhs,
            loc=loc,
            parent=parent,
        )


@public
@typechecked
class NotOp(BoolUnaryOp):
    """
    title: AST class for logical NOT operation.
    attributes:
      op_code:
        type: str
      operand:
        type: DataType
      kind:
        type: ASTKind
    """

    kind: ASTKind

    kind = ASTKind.NotOpKind
    op_code = "not"

    def __init__(
        self,
        operand: DataType,
        loc: SourceLocation = NO_SOURCE_LOCATION,
        parent: Optional[ASTNodes] = None,
    ) -> None:
        """
        title: Instantiate AST class for logical NOT operation.
        parameters:
          operand:
            type: DataType
          loc:
            type: SourceLocation
          parent:
            type: Optional[ASTNodes]
        """
        super().__init__(
            op_code=self.op_code,
            operand=operand,
            loc=loc,
            parent=parent,
        )
