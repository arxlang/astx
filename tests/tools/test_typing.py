from __future__ import annotations

from typing import Any

from astx.tools import typing


def test_skip_unused() -> None:
    any_var = None
    typing.skip_unused(any_var, **{"other_vars": None})


def test_copy_type() -> None:
    class A:
        def __init__(self, any_var: str = "") -> None:
            pass

    class B:
        @typing.copy_type(A.__init__)
        def __init__(self, *args: Any, **kwargs: Any) -> None:
            super().__init__(*args, **kwargs)
