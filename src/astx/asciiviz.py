"""
AST to ascii art Conversion Module.

This module provides utilities for converting an Abstract Syntax Tree (AST),
represented as a nested Python dictionary, to an ascii graph. The graph can be
displayed directly in the terminal window.

"""
from typing import Dict, List, Tuple

import networkx as nx

from asciinet import graph_to_ascii


def get_nodes_edges(
    dic: Dict[str, str],
    nodes: List[str] = [],
    edges: List[str] = [],
) -> Tuple[List[str], List[str]]:
    """
    Get nodes and edges needed for the ascii AST representation.

    Parameters
    ----------
    dic : dict
        The AST as a nested dictionary
    nodes : list, Optional
         list of nodes for the AST ascii representation. If present,
         nodes will be added to the existing ones.
    edges : list, Optional
         list of edges for the AST ascii representation. If present,
         edges will be added to the existing ones.

    Returns
    -------
    nodes: list
        list of nodes
    edges: list
        list of edges
    """
    for key, value in dic.items():
        nodes.append(key)
        if isinstance(value, dict):
            for value_key in list(value.keys()):
                edges.append((key, value_key))
            get_nodes_edges(value, nodes, edges)
        if isinstance(value, list):
            for list_item in value:
                if isinstance(list_item, dict):
                    for list_key in list(list_item.keys()):
                        edges.append((key, list_key))
                    get_nodes_edges(list_item, nodes, edges)
    return nodes, edges


def ascii_ast(nodes: List[str], edges: List[str]) -> None:
    """
    Create ascii AST representation.

    Parameters
    ----------
    nodes : list
         list of nodes for the AST ascii representation.
    edges : list
         list of edges for the AST ascii representation.
         Each item of the list must be a tuple.
    """
    G = nx.Graph()
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    print(graph_to_ascii)
