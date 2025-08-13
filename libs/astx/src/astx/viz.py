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


def _esc_mermaid_label(s: str) -> str:
    """Escape quotes for Mermaid labels (image/Jupyter path)."""
    return str(s).replace('"', r"\"")


def _traverse_ast_to_mermaid(
    ast: ReprStruct,
    *,
    direction: Direction = "TD",
    named_items: bool = True,
) -> str:
    """
    Convert AST to Mermaid.

    Parameters
    ----------
    direction : "TD" | "LR"
        Layout direction.
    named_items : bool
        If True, emit `ID["Label"]` node declarations and quoted edge labels
        (best for Jupyter/image). If False, emit plain identifiers and pipe
        edge labels (compatible with mermaid-ascii).
    """
    if direction not in ("TD", "LR"):
        raise ValueError('direction must be "TD" or "LR"')

    lines: list[str] = [f"graph {direction}"]

    def walk(
        node: ReprStruct,
        parent_id: Optional[str] = None,
        carry_edge_label: str = "",
    ) -> None:
        if not isinstance(node, dict):
            return

        for key, full_value in node.items():
            if not isinstance(full_value, dict):
                continue

            content = full_value.get("content", "")
            metadata = cast(
                DictDataTypesStruct, full_value.get("metadata", {})
            )

            # Edge-only dict: carry the key as the edge label to its children.
            if not metadata:
                walk(full_value, parent_id, carry_edge_label=key)
                continue

            ref = cast(str, metadata.get("ref", ""))

            if named_items:
                node_id = _stable_id(key, ref, content)
                # declare node with pretty label for Jupyter/image
                lines.append(f'{node_id}["{_esc_mermaid_label(key)}"]')
            else:
                node_id = key

            # connect from parent
            if parent_id:
                if carry_edge_label:
                    if named_items:
                        # quoted label variant, Jupyter mermaid renderer
                        # accepts it
                        lines.append(
                            f"{parent_id} -- "
                            f'"{_esc_mermaid_label(carry_edge_label)}"'
                            f" --> {node_id}"
                        )
                    else:
                        # pipe label variant (mermaid-ascii understands this)
                        # escape any pipe in the label by replacing with '/'
                        elabel = carry_edge_label.replace("|", "/")
                        lines.append(f"{parent_id} -->|{elabel}| {node_id}")
                else:
                    lines.append(f"{parent_id} --> {node_id}")

            # descend
            if isinstance(content, dict):
                walk(content, node_id, carry_edge_label="")
            elif isinstance(content, list):
                for item in content:
                    if isinstance(item, dict):
                        walk(item, node_id, carry_edge_label="")

    walk(ast, None, "")
    return "\n".join(lines) + "\n"


def ast_to_mermaid(ast: ReprStruct, direction: Direction = "TD") -> str:
    """Mermaid for Jupyter/image (uses named items)."""
    return _traverse_ast_to_mermaid(ast, direction=direction, named_items=True)


def ast_to_mermaid_ascii(ast: ReprStruct, direction: Direction = "TD") -> str:
    """Mermaid tailored for mermaid-ascii, no named items, pipe edge labels."""
    return _traverse_ast_to_mermaid(
        ast, direction=direction, named_items=False
    )


def visualize_image(ast: ReprStruct, direction: Direction = "TD") -> None:
    """Display the AST as Mermaid inline in Jupyter (Lab ≥4.1 / NB ≥7.1)."""
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
    border_padding: Optional[int] = 0,
    padding_x: Optional[int] = 3,
    padding_y: Optional[int] = 3,
    ascii_only: bool = False,
) -> str:
    """
    Render the AST to ASCII using the `mermaid-ascii` CLI.

    For maximum compatibility, this uses an ASCII-friendly Mermaid form:
    - no named items (node text is the identifier)
    - pipe-labeled edges (--> |label| ...)
    """
    exe = _find_mermaid_ascii()
    src = ast_to_mermaid_ascii(ast, direction=direction)

    cmd = [exe]
    if width is not None:
        cmd += ["-x", str(width)]
    if border_padding is not None:
        cmd += ["--borderPadding", str(border_padding)]
    if padding_x is not None:
        cmd += ["--paddingX", str(padding_x)]
    if padding_y is not None:
        cmd += ["--paddingY", str(padding_y)]
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
        first = src.splitlines()[0].strip() if src else ""
        hint = ""
        if "first line should define the graph" in (proc.stderr or ""):
            hint = f" (first line is {first!r}; try 'graph TD' or 'graph LR')"
        raise RuntimeError((proc.stderr or "mermaid-ascii failed.") + hint)

    if proc.stderr:
        raise RuntimeError(proc.stderr.strip())

    return proc.stdout
