"""
AST to Graphviz Conversion Module.

This module provides utilities for converting an Abstract Syntax Tree (AST),
represented as a nested Python dictionary, to a Graphviz dot graph. The graph
can be displayed inline in a Jupyter notebook.
"""
from typing import Optional

from graphviz import Digraph
from IPython.display import Image, display  # type: ignore[attr-defined]

from astx.base import ReprStruct


def traverse_ast(
    ast: ReprStruct,
    graph: Optional[Digraph] = None,
    parent: Optional[str] = None,
    shape: str = "box",
) -> Digraph:
    """
    Recursively traverse the AST and build a Graphviz graph.

    Parameters
    ----------
    ast : ReprStruct
        The AST as a nested dictionary.
    graph : Digraph
        The Graphviz graph object.
    parent : str, optional
        The identifier of the parent node in the graph, by default
        it is an empty string
    shape: str, options: ellipse, box, circle, diamond
        The shape used for the nodes in the graph. Default "box".
    """
    if not graph:
        graph = Digraph()

    if not isinstance(ast, dict):
        return graph

    for key, value in ast.items():
        node_name = f"{hash(key)}_{hash(str(value))}"
        graph.node(node_name, key, shape=shape)

        if parent:
            graph.edge(parent, node_name)

        if isinstance(value, dict):
            traverse_ast(value, graph, node_name, shape=shape)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    traverse_ast(item, graph, node_name, shape=shape)
    return graph


def visualize(ast: ReprStruct, shape: str = "box") -> None:
    """
    Visualize the AST using graphviz.

    Parameters
    ----------
    ast: ReprStruct
    shape: str, options: ellipse, box, circle, diamond
        The shape used for the nodes in the graph. Default "box".
    """
    graph = traverse_ast(ast, shape=shape)
    image = Image(graph.pipe(format="png"))  # type: ignore[no-untyped-call]
    display(image)  # type: ignore[no-untyped-call]
