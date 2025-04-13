"""Tests for collection objects."""

import astx

from astx.viz import visualize


def test_list_object_Literal_type_object() -> None:
    """Test list object having elements of literal type."""
    ls = astx.ObjectList(elements=[astx.LiteralInt32(1), astx.LiteralInt32(2)])
    print(ls)
    repr(ls)
    assert str(ls)
    assert ls.get_struct()
    assert ls.get_struct(simplified=True)
    visualize(ls.get_struct())


def test_list_object_object_type_collection() -> None:
    """Test list object having elements of Object collection type."""
    ls = astx.ObjectList(
        elements=[
            astx.ObjectList(
                elements=[astx.LiteralInt32(1), astx.LiteralInt32(2)]
            ),
            astx.ObjectList(
                elements=[astx.LiteralInt32(3), astx.LiteralInt32(4)]
            ),
        ]
    )
    print(ls)
    repr(ls)
    assert str(ls)
    assert ls.get_struct()
    assert ls.get_struct(simplified=True)
    visualize(ls.get_struct())


def test_tuple_object_Literal_type_object() -> None:
    """Test tuple object having elements of literal type."""
    tp = astx.ObjectTuple(
        elements=(astx.LiteralInt32(1), astx.LiteralInt32(2))
    )
    print(tp)
    repr(tp)
    assert str(tp)
    assert tp.get_struct()
    assert tp.get_struct(simplified=True)
    visualize(tp.get_struct())


def test_tuple_object_object_type_collection() -> None:
    """Test tuple object having elements of Object collection type."""
    tp = astx.ObjectTuple(
        elements=(
            astx.ObjectList(
                elements=[astx.LiteralInt32(1), astx.LiteralInt32(2)]
            ),
            astx.ObjectList(
                elements=[astx.LiteralInt32(3), astx.LiteralInt32(4)]
            ),
        )
    )
    print(tp)
    repr(tp)
    assert str(tp)
    assert tp.get_struct()
    assert tp.get_struct(simplified=True)
    visualize(tp.get_struct())


def test_set_object_Literal_type_object() -> None:
    """Test set object having elements of literal type."""
    st = astx.ObjectSet(elements={astx.LiteralInt32(1), astx.LiteralInt32(2)})
    print(st)
    repr(st)
    assert str(st)
    assert st.get_struct()
    assert st.get_struct(simplified=True)
    visualize(st.get_struct())


def test_set_object_object_type_collection() -> None:
    """Test set object having elements of Object collection type."""
    st = astx.ObjectSet(
        elements={
            astx.ObjectList(
                elements=[astx.LiteralInt32(1), astx.LiteralInt32(2)]
            ),
            astx.ObjectList(
                elements=[astx.LiteralInt32(3), astx.LiteralInt32(4)]
            ),
        }
    )
    print(st)
    repr(st)
    assert str(st)
    assert st.get_struct()
    assert st.get_struct(simplified=True)
    visualize(st.get_struct())


def test_dict_object_Literal_type_object() -> None:
    """Test dict object having elements of literal type."""
    dict = astx.ObjectDict(
        elements={
            astx.Variable("x"): astx.LiteralInt32(1),
            astx.Variable("y"): astx.LiteralInt32(2),
        }
    )
    print(dict)
    repr(dict)
    assert str(dict)
    assert dict.get_struct()
    assert dict.get_struct(simplified=True)
    visualize(dict.get_struct())
