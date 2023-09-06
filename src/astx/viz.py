"""
AST to Graphviz Conversion Module.

This module provides utilities for converting an Abstract Syntax Tree (AST),
represented as a nested Python dictionary, to a Graphviz dot graph. The graph
can be displayed inline in a Jupyter notebook.
"""
from typing import Optional

from graphviz import Digraph
from IPython.display import Image, display

from astx.base import ReprStruct


def traverse_ast(
    ast: ReprStruct,
    graph: Optional[Digraph] = None,
    parent: Optional[str] = None,
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
    """
    if not graph:
        graph = Digraph()

    if not isinstance(ast, dict):
        return graph

    for key, value in ast.items():
        node_name = f"{hash(key)}_{hash(str(value))}"
        graph.node(node_name, key)

        if parent:
            graph.edge(parent, node_name)

        if isinstance(value, dict):
            traverse_ast(value, graph, node_name)
        elif isinstance(value, list):
            for item in value:
                if isinstance(item, dict):
                    traverse_ast(item, graph, node_name)
    return graph


def visualize(ast: ReprStruct) -> None:
    """Visualize the AST using graphviz."""
    graph = traverse_ast(ast)
    display(Image(graph.pipe(format="png")))
