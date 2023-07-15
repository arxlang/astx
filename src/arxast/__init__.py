# mypy: disable-error-code="attr-defined"
"""Arx-AST."""
from importlib import metadata as importlib_metadata

from arxast import base
from arxast import blocks
from arxast import callables
from arxast import datatypes
from arxast import operators
from arxast import statements


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
