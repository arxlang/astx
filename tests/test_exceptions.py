"""Tests for exceptions classes."""

from astx.base import Identifier
from astx.blocks import Block
from astx.callables import (
    Argument,
    Arguments,
    Function,
    FunctionCall,
    FunctionPrototype,
)
from astx.exceptions import (
    CatchHandlerStmt,
    ExceptionHandlerStmt,
    FinallyHandlerStmt,
    ThrowStmt,
)
from astx.literals import LiteralString
from astx.types import String
from astx.viz import visualize


def test_throw_stmt() -> None:
    """Test `ThrowStmt` class."""
    # specify the exception to be thrown
    exc = Identifier("exception_message")

    # create the throw statement
    throw_stmt = ThrowStmt(exception=exc)

    assert str(throw_stmt)
    assert throw_stmt.get_struct()
    assert throw_stmt.get_struct(simplified=True)
    visualize(throw_stmt.get_struct())


def fn_print(
    arg: LiteralString,
) -> FunctionCall:
    """Return a FunctionCall to print a string."""
    proto = FunctionPrototype(
        name="print",
        args=Arguments(Argument("_", type_=String())),
        return_type=String(),
    )
    fn = Function(prototype=proto, body=Block())
    return FunctionCall(
        fn=fn,
        args=[arg],
    )


def test_catchhandler_stmt_onetype() -> None:
    """Test `CatchHandler` class with one type."""
    # Create the "except" block
    exception_types = [Identifier("A")]
    except_body1 = Block()
    except_body1.append(fn_print(LiteralString(value="passed")))

    handler1 = CatchHandlerStmt(
        name=Identifier("e"), types=exception_types, body=except_body1
    )
    assert str(handler1)
    assert handler1.get_struct()
    assert handler1.get_struct(simplified=True)
    visualize(handler1.get_struct())


def test_catchhandler_stmt_multipletypes() -> None:
    """Test `CatchHandler` class with multiple types."""
    # Create the "except" block
    exception_types = [Identifier("A"), Identifier("B")]
    except_body1 = Block()
    except_body1.append(fn_print(LiteralString(value="passed")))

    handler1 = CatchHandlerStmt(
        name=Identifier("e"), types=exception_types, body=except_body1
    )
    assert str(handler1)
    assert handler1.get_struct()
    assert handler1.get_struct(simplified=True)
    visualize(handler1.get_struct())


def test_catchhandler_stmt_notypes() -> None:
    """Test `CatchHandler` class without types."""
    # Create the "except" block
    except_body1 = Block()
    except_body1.append(fn_print(LiteralString(value="passed")))

    handler1 = CatchHandlerStmt(name=Identifier("e"), body=except_body1)
    assert str(handler1)
    assert handler1.get_struct()
    assert handler1.get_struct(simplified=True)
    visualize(handler1.get_struct())


def test_catchhandler_stmt_notypes_noname() -> None:
    """Test `CatchHandler` class without types or names."""
    # Create the "except" block
    except_body1 = Block()
    except_body1.append(fn_print(LiteralString(value="passed")))

    handler1 = CatchHandlerStmt(body=except_body1)
    assert str(handler1)
    assert handler1.get_struct()
    assert handler1.get_struct(simplified=True)
    visualize(handler1.get_struct())


def test_catchhandler_stmt_noname() -> None:
    """Test `CatchHandler` class without name."""
    # Create the "except" block
    exception_types = [Identifier("A")]
    except_body1 = Block()
    except_body1.append(fn_print(LiteralString(value="passed")))

    handler1 = CatchHandlerStmt(types=exception_types, body=except_body1)
    assert str(handler1)
    assert handler1.get_struct()
    assert handler1.get_struct(simplified=True)
    visualize(handler1.get_struct())


def test_exceptionhandler_stmt() -> None:
    """Test `ExceptionHandlerStmt` class with one handler."""
    exception_types = [Identifier("A")]

    # Create the "except" block
    except_body1 = Block()
    except_body1.append(fn_print(LiteralString(value="passed")))
    handler1 = CatchHandlerStmt(
        name=Identifier("e"), types=exception_types, body=except_body1
    )

    # Create the "try" block
    try_body = Block()
    try_body.append(fn_print(LiteralString(value="passed")))

    exc_handler = ExceptionHandlerStmt(body=try_body, handlers=[handler1])

    assert str(exc_handler)
    assert exc_handler.get_struct()
    assert exc_handler.get_struct(simplified=True)
    visualize(exc_handler.get_struct())


def test_exceptionhandler_stmt_multiplehandlers() -> None:
    """Test `ExceptionHandlerStmt` class with multiple handlers."""
    # Create the "except" block
    exception1_types = [Identifier("A")]
    except_body1 = Block()
    except_body1.append(fn_print(LiteralString(value="failed_block1")))
    handler1 = CatchHandlerStmt(
        name=Identifier("e"), types=exception1_types, body=except_body1
    )

    # Create another "except" block
    exception2_types = [Identifier("B")]

    except_body2 = Block()
    except_body2.append(fn_print(LiteralString(value="failed_block2")))

    handler2 = CatchHandlerStmt(types=exception2_types, body=except_body2)

    # Create the "try" block
    try_body = Block()
    try_body.append(fn_print(LiteralString(value="passed")))

    exc_handler = ExceptionHandlerStmt(
        body=try_body, handlers=[handler1, handler2]
    )

    assert str(exc_handler)
    assert exc_handler.get_struct()
    assert exc_handler.get_struct(simplified=True)
    visualize(exc_handler.get_struct())


def test_finallyhandler_stmt_() -> None:
    """Test `FinallyHandlerStmt` class."""
    # Create the "finally" block
    finally_body = Block()
    finally_body.append(fn_print(LiteralString(value="run complete")))

    finally_handler = FinallyHandlerStmt(body=finally_body)

    assert str(finally_handler)
    assert finally_handler.get_struct()
    assert finally_handler.get_struct(simplified=True)
    visualize(finally_handler.get_struct())


def test_exceptionhandler_stmt_multiplehandlers_finally() -> None:
    """Test `ExceptionHandlerStmt` class with multiple handlers and finally."""
    # Create the "except" block
    exception1_types = [Identifier("A")]
    except_body1 = Block()
    except_body1.append(fn_print(LiteralString(value="failed_block1")))
    handler1 = CatchHandlerStmt(
        name=Identifier("e"), types=exception1_types, body=except_body1
    )

    # Create another "except" block
    exception2_types = [Identifier("B")]

    except_body2 = Block()
    except_body2.append(fn_print(LiteralString(value="failed_block2")))

    handler2 = CatchHandlerStmt(types=exception2_types, body=except_body2)

    # Create the "finally" block
    finally_body = Block()
    finally_body.append(fn_print(LiteralString(value="run complete")))

    finally_handler = FinallyHandlerStmt(body=finally_body)

    # Create the "try" block
    try_body = Block()
    try_body.append(fn_print(LiteralString(value="passed")))

    exc_handler = ExceptionHandlerStmt(
        body=try_body,
        handlers=[handler1, handler2],
        finally_handler=finally_handler,
    )

    assert str(exc_handler)
    assert exc_handler.get_struct()
    assert exc_handler.get_struct(simplified=True)
    visualize(exc_handler.get_struct())
