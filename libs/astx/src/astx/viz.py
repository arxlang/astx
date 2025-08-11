"""
AST graphic representation Module.

This module provides utilities for converting an Abstract Syntax Tree (AST)
to Mermaid for inline display in Jupyter (Lab ≥4.1 / NB ≥7.1) and to ASCII
via the `mermaid-ascii` CLI.
"""

from __future__ import annotations

import hashlib
import shutil
import subprocess

from typing import Literal, Optional, cast

from IPython.display import display as _display

from astx.base import DictDataTypesStruct, ReprStruct

Direction = Literal["TD", "LR"]


def _stable_id(label: str, ref: str, content: object) -> str:
    """Build a stable-ish node id from label/ref/content."""
    h = hashlib.md5(
        f"{label}|{ref}|{type(content).__name__}|{content!r}".encode(),
        usedforsecurity=False,
    ).hexdigest()
    return f"N{h[:10]}"


def _esc(s: str) -> str:
    """Escape quotes for Mermaid labels."""
    return str(s).replace('"', r"\"")


def _traverse_ast_to_mermaid(
    ast: ReprStruct,
    lines: Optional[list[str]] = None,
    parent: Optional[str] = None,
    edge_label: str = "",
) -> list[str]:
    """
    DFS traversal that emits Mermaid node and edge lines.

    Notes
    -----
      - Expects the caller to initialize `lines` with the graph header.
      - Treats entries without 'metadata' as edge labels to their children.
    """
    if lines is None:
        # caller should pass the header; keep guard for safety
        lines = ["graph TD"]

    if not isinstance(ast, dict):
        return lines

    for key, full_value in ast.items():
        if not isinstance(full_value, dict):
            continue

        content = full_value.get("content", "")
        metadata = cast(DictDataTypesStruct, full_value.get("metadata", {}))

        # Edge-only dict: carry the key as the edge label downward.
        if not metadata:
            _traverse_ast_to_mermaid(full_value, lines, parent, edge_label=key)
            continue

        ref = cast(str, metadata.get("ref", ""))
        node_id = _stable_id(key, ref, content)
        lines.append(f'{node_id}["{_esc(key)}"]')

        if parent:
            if edge_label:
                lines.append(f'{parent} -- "{_esc(edge_label)}" --> {node_id}')
            else:
                lines.append(f"{parent} --> {node_id}")

        if isinstance(content, dict):
            _traverse_ast_to_mermaid(content, lines, parent=node_id)
        elif isinstance(content, list):
            for item in content:
                if isinstance(item, dict):
                    _traverse_ast_to_mermaid(item, lines, parent=node_id)

    return lines


def ast_to_mermaid(ast: ReprStruct, direction: Direction = "TD") -> str:
    """
    Convert an AST (ReprStruct) into a Mermaid graph definition.

    Parameters
    ----------
    ast : ReprStruct
        The AST structure.
    direction : Literal["TD", "LR"]
        Mermaid layout direction. Use "TD" (top-down) or "LR" (left-right).

    Returns
    -------
    str
        Mermaid source text starting with `graph TD` or `graph LR`.
    """
    if direction not in ("TD", "LR"):
        raise ValueError('direction must be "TD" or "LR"')
    lines: list[str] = [f"graph {direction}"]
    _traverse_ast_to_mermaid(ast, lines=lines)
    # ensure trailing newline so some parsers don't choke on last line
    return "\n".join(lines) + "\n"


def visualize_image(ast: ReprStruct, direction: Direction = "TD") -> None:
    """
    Display the AST as Mermaid inline in Jupyter (Lab ≥4.1 / NB ≥7.1).

    Parameters
    ----------
    ast : ReprStruct
        The AST structure.
    direction : Literal["TD", "LR"]
        Layout direction for the rendered graph.
    """
    _display(  # type: ignore
        {"text/vnd.mermaid": ast_to_mermaid(ast, direction=direction)},
        raw=True,
    )


def _find_mermaid_ascii() -> str:
    """Resolve the `mermaid-ascii` CLI path or raise a clear error."""
    exe = shutil.which("mermaid-ascii") or shutil.which("mermaid-ascii.exe")
    if not exe:
        raise RuntimeError(
            "mermaid-ascii CLI not found. Install the PyPI package that ships "
            "the binary, or put `mermaid-ascii` on PATH."
        )
    return exe


def visualize_ascii(
    ast: ReprStruct,
    timeout: int = 10,
    direction: Direction = "TD",
    width: Optional[int] = None,
    padding: Optional[int] = None,
    ascii_only: bool = False,
) -> str:
    """
    Render the AST to ASCII using the `mermaid-ascii` CLI.

    Parameters
    ----------
    ast : ReprStruct
        The AST structure.
    timeout : int
        Subprocess timeout in seconds (default 10).
    direction : Literal["TD", "LR"]
        Layout direction passed via the Mermaid header.
    width : Optional[int]
        Extra horizontal spacing (maps to `-x` in mermaid-ascii). None default.
    padding : Optional[int]
        Box padding (maps to `-p` in mermaid-ascii). None = default.
    ascii_only : bool
        If True, add `--ascii` to force ASCII (no Unicode box characters).

    Returns
    -------
    str
        The ASCII diagram string.

    Raises
    ------
    RuntimeError
        If the `mermaid-ascii` process fails.
    """
    exe = _find_mermaid_ascii()
    src = ast_to_mermaid(ast, direction=direction)

    cmd = [exe]
    if width is not None:
        cmd += ["-x", str(width)]
    if padding is not None:
        cmd += ["-p", str(padding)]
    if ascii_only:
        cmd += ["--ascii"]

    proc = subprocess.run(
        cmd,
        input=src,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        timeout=timeout,
        check=False,
    )

    if proc.returncode != 0:
        # Provide a helpful hint if the header is wrong.
        hint = ""
        first = src.splitlines()[0].strip() if src else ""
        if "first line should define the graph" in (proc.stderr or ""):
            hint = f" (first line is {first!r}; try 'graph TD' or 'graph LR')"
        raise RuntimeError((proc.stderr or "mermaid-ascii failed.") + hint)

    if proc.stderr:
        # treat non-empty stderr as error; keeps behavior explicit
        raise RuntimeError(proc.stderr.strip())

    return proc.stdout
