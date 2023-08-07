# mypy: disable-error-code="attr-defined"
"""ASTx."""
from importlib import metadata as importlib_metadata

from astx import base  # noqa: F401
from astx import blocks  # noqa: F401
from astx import callables  # noqa: F401
from astx import datatypes  # noqa: F401
from astx import flows  # noqa: F401
from astx import mixes  # noqa: F401
from astx import operators  # noqa: F401
from astx import symbol_table  # noqa: F401
from astx import variables  # noqa: F401


def get_version() -> str:
    """Return the program version."""
    try:
        return importlib_metadata.version(__name__)
    except importlib_metadata.PackageNotFoundError:  # pragma: no cover
        return "0.1.0"  # semantic-release


version: str = get_version()

__author__ = "Ivan Ogasawara"
__email__ = "ivan.ogasawara@gmail.com"
__version__: str = version
