# visualize.py
"""
Visualization with improved layout and optional sparsification (k-NN edges).
- Uses a stronger spring layout + iterative repulsion to reduce overlap.
- Optionally draws only k nearest neighbor edges per node (reduces clutter).
- Keeps colored circular nodes, labels inside nodes, and highlighted path.
- Saves images to outputs/.
"""

import os
import math
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors

OUTDIR = "outputs"
os.makedirs(OUTDIR, exist_ok=True)


def _node_color_map(nodes):
    cmap = cm.get_cmap("tab20")
    N = len(nodes)
    return [mcolors.to_hex(cmap(i % cmap.N)) for i in range(N)]


def _separate_positions(pos, node_sizes, iterations=400, min_scale=0.20):
    nodes = list(pos.keys())
    coords = np.array([pos[n] for n in nodes], dtype=float)
    radii = np.array([node_sizes[n] for n in nodes], dtype=float)

    for _ in range(iterations):
        dx = coords[:, None, 0] - coords[None, :, 0]
        dy = coords[:, None, 1] - coords[None, :, 1]
        dist = np.hypot(dx, dy) + 1e-9
        required = (radii[:, None] + radii[None, :]) * (1.0 + min_scale)
        overlap = required - dist
        mask = overlap > 0
        if not mask.any():
            break
        disp_x = (dx / dist) * (overlap * 0.5)
        disp_y = (dy / dist) * (overlap * 0.5)
        move_x = np.where(mask, disp_x, 0.0).sum(axis=1)
        move_y = np.where(mask, disp_y, 0.0).sum(axis=1)
        coords += np.stack([move_x, move_y], axis=1) * 0.18

    return {n: coords[i] for i, n in enumerate(nodes)}


def _compute_layout(G, node_size_map, seed=1):
    n = max(1, G.number_of_nodes())
    # stronger spacing for larger graphs
    k = 1.0 / (math.sqrt(n) * 0.45)
    # use larger scale and more iterations for better initial spread
    pos = nx.spring_layout(G, seed=seed, k=k, iterations=1200, scale=4.0)
    adjusted = _separate_positions(pos, node_size_map, iterations=400, min_scale=0.20)
    return adjusted


def _k_nearest_edges(G, k=4):
    """
    Return a set of edges (u,v) representing the k nearest neighbors for each node,
    measured by weight (smaller distance = nearer). This is used to *visualize* a
    sparse subset of edges while keeping important local structure.
    """
    if k is None:
        return set((u, v) for u, v in G.edges())

    knn_edges = set()
    for u in G.nodes():
        # get neighbors and weights
        nbrs = []
        for v in G.neighbors(u):
            w = G[u][v].get('weight', 1.0)
            nbrs.append((w, v))
        nbrs.sort(key=lambda x: x[0])  # sort by distance (small->near)
        for _, v in nbrs[:k]:
            knn_edges.add((u, v))
    # make undirected by including both orientations
    knn_edges |= set((b, a) for (a, b) in knn_edges)
    return knn_edges


def draw_graph(G, title="City Graph", node_size=700, fname="graph.png",
               highlight_path=None, sparsify_k=4):
    """
    Draws the graph with reduced clutter:
    - sparsify_k: number of nearest neighbors to draw per node (None => draw all edges)
    - node_size: controls circle size (affects spacing)
    - highlight_path: list of node names (ordered) to highlight
    Returns saved filepath.
    """
    nodes = list(G.nodes())
    # radius used for collision avoidance (tuned)
    node_size_map = {n: max(6.0, math.sqrt(node_size) * 0.10) for n in nodes}

    pos = _compute_layout(G, node_size_map, seed=1)
    plt.figure(figsize=(14, 10))
    node_colors = _node_color_map(nodes)

    # determine which edges to draw (sparsified)
    knn_edges = _k_nearest_edges(G, k=sparsify_k)

    # determine path edges
    path_edges = set()
    if highlight_path and len(highlight_path) >= 2:
        path_edges = set(zip(highlight_path, highlight_path[1:]))
        path_edges |= set((b, a) for (a, b) in path_edges)

    # non-path edges from chosen set
    non_path_edges = [(u, v) for (u, v) in knn_edges if (u, v) not in path_edges and (v, u) not in path_edges]
    if non_path_edges:
        nx.draw_networkx_edges(G, pos, edgelist=non_path_edges, edge_color="#d9d9d9", alpha=0.6, width=0.9)

    # draw path edges (even if they weren't in knn_edges)
    if path_edges:
        # ensure path edges are drawn (add them to path_edges_list)
        nx.draw_networkx_edges(G, pos, edgelist=list(path_edges), edge_color="#d62728", width=3.0, alpha=0.95)

    # draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_colors,
                           edgecolors="black", linewidths=0.8)

    # labels inside nodes (fontsize scales with node_size)
    base_font = max(6, min(12, int(math.sqrt(node_size) / 2.6)))
    for n, c in zip(nodes, node_colors):
        x, y = pos[n]
        plt.text(x, y, str(n), ha="center", va="center", fontsize=base_font, fontweight="bold",
                 color="white", bbox=dict(boxstyle="circle,pad=0.3", facecolor=c, edgecolor="none"))

    plt.title(title, fontsize=12, fontweight="bold")
    plt.axis("off")
    plt.tight_layout()

    outpath = os.path.join(OUTDIR, fname)
    plt.savefig(outpath, dpi=160)
    plt.close()
    return outpath


def draw_path(G, path, title="Path", fname="path.png", sparsify_k=4):
    return draw_graph(G, title=title, node_size=900, fname=fname, highlight_path=path, sparsify_k=sparsify_k)
