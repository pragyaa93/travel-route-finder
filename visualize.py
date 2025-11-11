# visualize.py
"""
Enhanced Codespaces-friendly visualization:
- Bigger nodes
- Distinct colors per node
- City label inside the node (circular label background)
- Highlighted path (different color + thicker)
Saves images to 'outputs/'.
"""

import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import os

OUTDIR = "outputs"
os.makedirs(OUTDIR, exist_ok=True)

def _node_color_map(nodes):
    """Return a color for each node using a colormap."""
    cmap = cm.get_cmap("tab20")  # good variety of distinct colors
    N = len(nodes)
    colors = []
    for i, n in enumerate(nodes):
        colors.append(mcolors.to_hex(cmap(i % cmap.N)))
    return colors

def draw_graph(G, title="City Graph", show_weights=True,
               node_size=900, fname="graph.png", highlight_path=None):
    """
    Draw the full graph.
    - node_size: controls node diameter (default bigger).
    - highlight_path: if provided, should be a list of node names representing a path to highlight.
    """
    pos = nx.spring_layout(G, seed=1)  # deterministic layout

    plt.figure(figsize=(14,10))
    nodes = list(G.nodes())
    node_colors = _node_color_map(nodes)

    # Draw non-path edges dimly first
    all_edges = list(G.edges(data=True))
    path_edges = set()
    if highlight_path and len(highlight_path) >= 2:
        path_edges = set(zip(highlight_path, highlight_path[1:]))
        # also include reverse direction since graph is undirected
        path_edges |= set((b,a) for (a,b) in path_edges)

    non_path_edges = [ (u,v) for u,v,d in all_edges if (u,v) not in path_edges and (v,u) not in path_edges ]
    nx.draw_networkx_edges(G, pos, edgelist=non_path_edges, edge_color="#cccccc", alpha=0.7)

    # Draw path edges with distinct style if any
    if path_edges:
        path_edges_list = list(path_edges)
        nx.draw_networkx_edges(G, pos, edgelist=path_edges_list, edge_color="#d62728", width=3.0, alpha=0.95)

    # Draw nodes (with node color)
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_colors, edgecolors="black", linewidths=0.6)

    # Draw labels centered INSIDE nodes
    labels = {n: n for n in nodes}
    # For label backgrounds, we create a bbox per node using the node color
    for n, c in zip(nodes, node_colors):
        x, y = pos[n]
        plt.text(x, y, str(n),
                 horizontalalignment='center',
                 verticalalignment='center',
                 fontsize=8,
                 fontweight='bold',
                 color='white',
                 bbox=dict(boxstyle='circle,pad=0.3', facecolor=c, edgecolor='none'))

    # Optionally draw weights (small, on non-path edges)
    if show_weights:
        # build a label dict for edges
        edge_labels = {}
        for u, v, d in G.edges(data=True):
            edge_labels[(u, v)] = int(d.get('weight', 0))
        # show edge labels lightly
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, label_pos=0.5, font_color="#666666")

    plt.title(title)
    plt.axis('off')
    plt.tight_layout()

    outpath = os.path.join(OUTDIR, fname)
    plt.savefig(outpath, dpi=160)
    plt.close()
    return outpath

def draw_path(G, path, title="Path", fname="path.png"):
    """
    Draw the graph but emphasize the given path.
    - path: list of node names in order.
    """
    return draw_graph(G, title=title, show_weights=True, node_size=1000, fname=fname, highlight_path=path)

