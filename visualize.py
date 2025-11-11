# visualize.py
"""
Simple visualization functions. Not geographic; uses graph layouts.
"""

import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(G, title="City Graph", show_weights=True, node_size=200):
    pos = nx.spring_layout(G, seed=1)  # deterministic layout
    plt.figure(figsize=(12,9))
    nx.draw_networkx_nodes(G, pos, node_size=node_size)
    nx.draw_networkx_labels(G, pos, font_size=8)
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    if show_weights:
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels={k: int(v) for k,v in labels.items()}, font_size=7)
    plt.title(title)
    plt.axis('off')
    plt.tight_layout()
    plt.show()

def draw_path(G, path, title="Path"):
    H = nx.path_graph(path)
    # create a subgraph with same node names in G coordinates
    pos = nx.spring_layout(G, seed=1)
    plt.figure(figsize=(10,6))
    nx.draw_networkx_nodes(G, pos, node_size=100)
    nx.draw_networkx_labels(G, pos, font_size=7)
    nx.draw_networkx_edges(G, pos, alpha=0.2)
    # draw path
    path_edges = list(zip(path, path[1:]))
    nx.draw_networkx_edges(G, pos, edgelist=path_edges, width=2.5)
    plt.title(title)
    plt.axis('off')
    plt.show()
