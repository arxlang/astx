# mypy: disable-error-code="attr-defined"
"""ASTx."""
from importlib import metadata as importlib_metadata

from astx import base
from astx import blocks
from astx import callables
from astx import datatypes
from astx import operators
from astx import statements
from astx import mixes


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
