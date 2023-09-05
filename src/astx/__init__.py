# mypy: disable-error-code="attr-defined"
"""ASTx."""
from importlib import metadata as importlib_metadata

from astx import (
    base,  # noqa: F401
    blocks,  # noqa: F401
    callables,  # noqa: F401
    datatypes,  # noqa: F401
    flows,  # noqa: F401
    mixes,  # noqa: F401
    operators,  # noqa: F401
    symbol_table,  # noqa: F401
    variables,  # noqa: F401
)


def get_version() -> str:
    """Return the program version."""
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "0.4.0"  # semantic-release


version: str = get_version()

__author__ = "Ivan Ogasawara"
__email__ = "ivan.ogasawara@gmail.com"
__version__: str = version
