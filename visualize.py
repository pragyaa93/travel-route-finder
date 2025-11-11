# visualize.py
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import os

OUTDIR = "outputs"
os.makedirs(OUTDIR, exist_ok=True)

def _node_color_map(nodes):
    cmap = cm.get_cmap("tab20")
    N = len(nodes)
    return [mcolors.to_hex(cmap(i % cmap.N)) for i in range(N)]

def draw_graph(G, title="City Graph", node_size=900, fname="graph.png", highlight_path=None):
    """
    Draw the graph:
    - Colorful circular nodes
    - City names inside nodes
    - Highlighted path (if provided)
    - No edge weights shown
    """
    pos = nx.spring_layout(G, seed=1)  # deterministic layout

    plt.figure(figsize=(14,10))
    nodes = list(G.nodes())
    node_colors = _node_color_map(nodes)

    # Highlight path
    all_edges = list(G.edges(data=True))
    path_edges = set()
    if highlight_path and len(highlight_path) >= 2:
        path_edges = set(zip(highlight_path, highlight_path[1:]))
        path_edges |= set((b,a) for (a,b) in path_edges)

    # Non-path edges (gray)
    non_path_edges = [(u,v) for u,v,d in all_edges if (u,v) not in path_edges and (v,u) not in path_edges]
    nx.draw_networkx_edges(G, pos, edgelist=non_path_edges, edge_color="#cccccc", alpha=0.4, width=0.8)

    # Path edges (red, thick)
    if path_edges:
        nx.draw_networkx_edges(G, pos, edgelist=list(path_edges), edge_color="#d62728", width=3.0, alpha=0.9)

    # Nodes
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_colors, edgecolors="black", linewidths=0.7)

    # City labels inside nodes
    for n, c in zip(nodes, node_colors):
        x, y = pos[n]
        plt.text(x, y, n, ha='center', va='center', fontsize=8, fontweight='bold',
                 color='white',
                 bbox=dict(boxstyle='circle,pad=0.3', facecolor=c, edgecolor='none'))

    plt.title(title, fontsize=12, fontweight='bold')
    plt.axis('off')
    plt.tight_layout()

    outpath = os.path.join(OUTDIR, fname)
    plt.savefig(outpath, dpi=160)
    plt.close()
    return outpath

def draw_path(G, path, title="Path", fname="path.png"):
    return draw_graph(G, title=title, node_size=1000, fname=fname, highlight_path=path)
