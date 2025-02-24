"""
AST graphic representation Module.

This module provides utilities for converting an Abstract Syntax Tree (AST),
represented as a nested Python dictionary, to a Graphviz dot graph which
can be displayed inline in a Jupyter notebook, or as an ascii representation
directly in the console.
"""

from __future__ import annotations

import re
import types

from typing import Optional, cast

import requests

from asciinet import (
    Timeout,
    _asciigraph,
    _AsciiGraphProxy,
)
from graphviz import Digraph
from IPython.display import Image, display
from msgpack import dumps, loads

from astx.base import DictDataTypesStruct, ReprStruct


def traverse_ast_ascii(
    ast: ReprStruct,
    graph: Optional[Digraph] = None,
    parent: Optional[str] = None,
    shape: str = "box",
) -> Digraph:
    """
    Traverse the AST and build a Graphviz graph for ascii representation.

    Parameters
    ----------
    ast : dict
        The AST as a nested dictionary (full structure version).
    graph : Digraph
        The Graphviz graph object.
    parent : str, optional
        The identifier of the parent node in the graph, by default
        it is an empty string
    shape: str, options: ellipse, box, circle, diamond
        The shape used for the nodes in the graph. Default "box".

    Returns
    -------
    Digraph
        Graphviz (dot) graph representation.
    """
    if not graph:
        graph = Digraph()
        graph.attr(rankdir="TB")

    if isinstance(ast, list):
        for item in ast:
            traverse_ast_ascii(cast(ReprStruct, item), graph, parent, shape)
    elif isinstance(ast, dict):
        for key, value in ast.items():
            if not parent:
                node_name = f"{hash(key)}"
            else:
                if parent.find("_"):
                    node_name = f"{parent[parent.find('_') + 1 :]}_{hash(key)}"
                else:
                    node_name = f"{parent}_{hash(key)}"
                graph.edge(parent, node_name)

            graph.node(node_name, label=key, shape=shape)
            traverse_ast_ascii(
                cast(ReprStruct, value), graph, node_name, shape
            )
    return graph


def traverse_ast_to_graphviz(
    ast: ReprStruct,
    graph: Optional[Digraph] = None,
    parent: Optional[str] = None,
    shape: str = "box",
    edge_label: str = "",
) -> Digraph:
    """
    Traverse the AST and build a Graphviz graph for png representation.

    Parameters
    ----------
    ast : dict
        The AST as a nested dictionary (full structure version).
    graph : Digraph
        The Graphviz graph object.
    parent : str, optional
        The identifier of the parent node in the graph, by default
        it is an empty string
    shape: str, options: ellipse, box, circle, diamond
        The shape used for the nodes in the graph. Default "box".

    Returns
    -------
    Digraph
        Graphviz (dot) graph representation.
    """
    if not graph:
        graph = Digraph()
        graph.attr(rankdir="TB")

    if not isinstance(ast, dict):
        return graph.unflatten(stagger=3)

    for key, full_value in ast.items():
        if not isinstance(full_value, dict):
            continue

        content = full_value.get("content", "")
        metadata = cast(DictDataTypesStruct, full_value.get("metadata", {}))
        ref = ""

        if not metadata:
            # if the node doesn't have a metadata, it is a edge
            traverse_ast_to_graphviz(
                full_value,
                graph,
                parent,
                shape=shape,
                edge_label=key,
            )
            continue

        ref = cast(str, metadata.get("ref", ""))

        node_name = f"{hash(key)}_{hash(str(ref))}_{hash(str(content))}"
        graph.node(node_name, key, shape=shape)

        if parent:
            graph_params = {"label": edge_label} if edge_label else {}
            graph.edge(parent, node_name, **graph_params)

        if isinstance(content, dict):
            traverse_ast_to_graphviz(content, graph, node_name, shape=shape)
            continue
        elif not isinstance(content, list):
            continue

        for item in content:
            if isinstance(item, dict):
                traverse_ast_to_graphviz(item, graph, node_name, shape=shape)
    return graph


def visualize(ast: ReprStruct, shape: str = "box") -> None:
    """
    Visualize the abstract syntax tree (AST) using graphviz.

    Parameters
    ----------
    ast: dict
            The AST as a nested dictionary
    shape: str, options: ellipse, box, circle, diamond.
        The shape used for the nodes in the graph. Default "box".
    """
    graph = traverse_ast_to_graphviz(ast, shape=shape)
    image = Image(  # type: ignore[no-untyped-call]
        graph.unflatten(stagger=3).pipe(format="png")
    )
    display(image)  # type: ignore[no-untyped-call]


def make_node_box(modhash_label_mapping: list[tuple[str, str]]) -> str:
    """
    Make ascii representation for one-node ASTs.

    Parameters
    ----------
    modhash_label_mapping : list
        Mapping between node hash and label.

    Returns
    -------
    str
        The ascii graph representation as a string.

    """
    label = modhash_label_mapping[0][1]
    box_width = len(label) + 2
    space_before_box = " " * 4
    box_upper = space_before_box + "┌" + "─" * box_width + "┐"
    box_middle = space_before_box + "│ " + label + " │"
    box_lower = space_before_box + "└" + "─" * box_width + "┘"
    box = [box_upper, box_middle, box_lower]
    node = "\n".join(box)
    return node


def graph_to_ascii_overload(
    self: _AsciiGraphProxy, graph: Digraph, timeout: int = 10
) -> str:
    """
    Overload asciinet.graph_to_ascii function.

    Create an ascii representation of the abstract syntax tree (AST).
    This function is suitable for usage with ASTs with multiple nodes
    with the same label.

    Parameters
    ----------
    graph : Digraph
        The Graphviz graph object.
    timeout : int
        Time limit in seconds for requests.post. Default is 10 seconds.

    Returns
    -------
    str
        The ascii graph representation as a string.

    """
    try:
        nodes_modhash, edges_modhash, modhash_label_mapping = get_hash_labels(
            graph
        )

        # assuming there won't be more than one node with no edges
        if not edges_modhash:
            node = make_node_box(modhash_label_mapping)
            return node

        # Prepare the graph ascii repr
        graph_repr = dumps({"vertices": nodes_modhash, "edges": edges_modhash})
        response = requests.post(self._url, data=graph_repr, timeout=timeout)
        success = 200
        if response.status_code == success:
            graph_str = loads(response.content)
        else:
            raise ValueError(
                "Internal error: \n{0}".format(response.content.decode())
            )

        # substitute modhash by labels in the ascii representation
        graph_list = list(graph_str)
        for modhash, label in modhash_label_mapping:
            start = graph_str.index(modhash)
            end = graph_str.index(modhash) + (len(modhash))
            graph_list[start:end] = label

        graph = "".join(graph_list)
        return graph  # type: ignore[no-any-return]

    except (ConnectionError, Timeout):
        self._restart()
        raise ValueError("Could not convert graph to ASCII")


def get_hash_labels(
    graph: Digraph,
) -> tuple[list[str], list[tuple[str, str]], list[tuple[str, str]]]:
    """
    Get hash and labels from Digraph for ascii AST representation.

    Parameters
    ----------
    graph : Digraph
        The Graphviz graph object.

    Returns
    -------
    list
        Hash for ascii representation nodes.
    list
        Hash for ascii representation edges.
    list
        Mapping between nodes hash and labels.
    """
    dot_lines = graph.source.splitlines()
    nodes_modhash = []
    edges_modhash = []
    sources_hash = []
    targets_hash = []
    modhash_label_mapping = []
    hash_modhash_mapping = []

    for dot_line in dot_lines:
        line = dot_line.strip().strip(";")
        if "label" in line:
            node_label = re.findall(r"(?<=label=).*(?= )", line)[0].replace(
                '"', ""
            )

            # all labels must be at least 7 characters long
            node_label = node_label.center(7, " ")
            len_label = len(node_label)

            # each node modhash will have the same length as the node label
            # and will consist of parts of the hash from both the parent
            # (if it exists) and child nodes, separated by underscore.
            node_hash = line.split("[")[0].strip().replace('"', "")
            if "_" not in node_hash:  # if it's the first node
                if len_label <= len(node_hash):
                    x = len_label
                    node_modhash = node_hash[:x]
                else:
                    node_modhash = node_hash + " " * (
                        len_label - len(node_hash)
                    )
            else:  # if it's connected before and after
                hash1, hash2 = node_hash.split("_")
                len_hash2 = len(hash2)
                len_hash1 = len(hash1)
                min_chars_hash1 = 3

                standard_label_len = (min_chars_hash1 + len_hash2) + 1
                long_label_len = len_hash1 + len_hash2 + 1
                # short label:
                # modhash will have 3 chars of hash1 and some part of hash2
                if len_label <= standard_label_len:
                    nchars_hash2 = len_label - (min_chars_hash1 + 1)
                    node_modhash = (
                        f"{hash1[:min_chars_hash1]}_{hash2[:nchars_hash2]}"
                    )
                # medium label:
                # modhash will have more than 3 chars of hash1 and all of hash2
                elif (len_label > standard_label_len) & (
                    len_label <= long_label_len
                ):
                    nchars_hash1 = (
                        len_label - standard_label_len + min_chars_hash1
                    )
                    node_modhash = f"{hash1[:nchars_hash1]}_{hash2}"
                # long label:
                # modhash will have all of hash1, all of hash2,
                # plus some additional chars
                else:
                    nchars = len_label - long_label_len
                    add_chars = "x" * nchars
                    node_modhash = f"{hash1}_{hash2}{add_chars}"

            nodes_modhash.append(node_modhash)
            hash_modhash_mapping.append((node_hash, node_modhash))
            modhash_label_mapping.append((node_modhash, node_label))

        elif "->" in line:
            source_hash, target_hash = line.split("->")
            sources_hash.append(source_hash.strip().replace('"', ""))
            targets_hash.append(target_hash.strip().replace('"', ""))

    for source_hash, target_hash in zip(sources_hash, targets_hash):
        source_modhash = next(
            modhash
            for hash_, modhash in hash_modhash_mapping
            if source_hash == hash_
        )
        target_modhash = next(
            modhash
            for hash_, modhash in hash_modhash_mapping
            if target_hash == hash_
        )

        edges_modhash.append((source_modhash, target_modhash))

    return nodes_modhash, edges_modhash, modhash_label_mapping


def graph_to_ascii(graph: Digraph, timeout: int = 10) -> str:
    """
    Wrap function for graph_to_ascii.

    Create an ascii representation of the abstract syntax tree (AST).

    Parameters
    ----------
    graph : Digraph
        The Graphviz graph object.
    timeout : int
        Time limit in seconds for requests.post. Default is 10 seconds.
    """
    if not isinstance(graph, Digraph):
        raise ValueError(
            f"Graph must be a graphviz.Digraph (`{type(graph)}` was given.)"
        )

    result = _asciigraph.graph_to_ascii(graph, timeout=timeout)
    return f"\n{result}\n"


_asciigraph.graph_to_ascii = types.MethodType(
    graph_to_ascii_overload, _asciigraph
)
