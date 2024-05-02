"""Test functions about typing."""

from __future__ import annotations

from typing import Any

from astx.tools import typing


def test_skip_unused() -> None:
    """Test the skip_unused function."""
    any_var = None
    typing.skip_unused(any_var, **{"other_vars": None})


def test_copy_type() -> None:
    """Test the copy_type function."""

    class A:
        """Class A."""

        def __init__(self, any_var: str = "") -> None:
            """Initialize class A."""
            pass

    class B:
        """Class B."""

        @typing.copy_type(A.__init__)
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            """Initialize class B."""
            super().__init__(*args, **kwargs)
