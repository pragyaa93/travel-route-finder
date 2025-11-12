# visualize.py
"""
Improved visualization with collision-avoidance to reduce overlapping nodes.
- Uses a stronger spring layout and then a small repulsion pass to separate nodes.
- Colored circular nodes with city names inside.
- Highlighted path in red.
- Saves to outputs/ folder.
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


def _separate_positions(pos, node_sizes, iterations=120, min_scale=0.14):
    """
    Simple iterative repulsion to reduce overlapping nodes.

    pos: dict[node] = np.array([x,y])
    node_sizes: dict[node] = radius-like (float)
    iterations: number of repulsion iterations
    min_scale: minimum separation factor baseline (tweak to increase spacing)
    """
    nodes = list(pos.keys())
    coords = np.array([pos[n] for n in nodes], dtype=float)
    radii = np.array([node_sizes[n] for n in nodes], dtype=float)

    for _ in range(iterations):
        # compute pairwise vectors
        dx = coords[:, None, 0] - coords[None, :, 0]  # shape (N,N)
        dy = coords[:, None, 1] - coords[None, :, 1]
        dist = np.hypot(dx, dy) + 1e-9  # avoid div 0
        # required minimal distance between centers
        required = (radii[:, None] + radii[None, :]) * (1.0 + min_scale)
        # where overlap occurs
        overlap = required - dist
        mask = overlap > 0
        if not mask.any():
            break
        # compute displacement vectors for overlapping pairs
        disp_x = (dx / dist) * (overlap * 0.5)
        disp_y = (dy / dist) * (overlap * 0.5)
        # sum displacements for each node
        move_x = np.where(mask, disp_x, 0.0).sum(axis=1)
        move_y = np.where(mask, disp_y, 0.0).sum(axis=1)
        # apply small step (dampen movement)
        coords += np.stack([move_x, move_y], axis=1) * 0.2

    # return back as dict
    return {n: coords[i] for i, n in enumerate(nodes)}


def _compute_layout(G, node_size_map, seed=1):
    """
    Compute positions with spring layout then apply collision-avoidance.
    node_size_map: dict node -> radius (units arbitrary, used for separation)
    """
    n = max(1, G.number_of_nodes())
    # choose k roughly proportional to sqrt(area)/n ~ 1/sqrt(n) scaled up
    k = 1.0 / (math.sqrt(n) * 0.5)  # increase k for more spacing for larger graphs
    # use a larger scale so coordinates are spread out
    pos = nx.spring_layout(G, seed=seed, k=k, iterations=800, scale=3.0)
    # convert node_size_map (which is radius-like) to same coordinate units
    adjusted = _separate_positions(pos, node_size_map, iterations=200, min_scale=0.12)
    return adjusted


def draw_graph(G, title="City Graph", node_size=900, fname="graph.png", highlight_path=None):
    """
    Draw the graph:
    - node_size: base size used to compute label radius. Actual plotting uses same node_size param.
    - highlight_path: list of node names (in order) to highlight.
    - Saves to outputs/<fname>.
    """
    # compute per-node radius (for collision avoidance). radius units are arbitrary
    # We scale radius from node_size so larger node_size => larger separation.
    nodes = list(G.nodes())
    # radius used in separation algorithm (tuned empirically)
    node_size_map = {n: max(6.0, math.sqrt(node_size) * 0.11) for n in nodes}

    # compute layout (spring + separation)
    pos = _compute_layout(G, node_size_map, seed=1)

    plt.figure(figsize=(14, 10))
    node_colors = _node_color_map(nodes)

    # determine path edges
    all_edges = list(G.edges(data=True))
    path_edges = set()
    if highlight_path and len(highlight_path) >= 2:
        path_edges = set(zip(highlight_path, highlight_path[1:]))
        path_edges |= set((b, a) for (a, b) in path_edges)

    # draw non-path edges (light gray)
    non_path_edges = [(u, v) for (u, v, d) in all_edges if (u, v) not in path_edges and (v, u) not in path_edges]
    if non_path_edges:
        nx.draw_networkx_edges(G, pos, edgelist=non_path_edges, edge_color="#d9d9d9", alpha=0.6, width=0.8, min_source_margin=5, min_target_margin=5)

    # draw highlighted path edges
    if path_edges:
        nx.draw_networkx_edges(G, pos, edgelist=list(path_edges), edge_color="#d62728", width=3.0, alpha=0.95)

    # draw nodes (colored)
    nx.draw_networkx_nodes(G, pos, node_size=node_size, node_color=node_colors, edgecolors="black", linewidths=0.8)

    # labels inside nodes - adjust fontsize to fit node_size
    # fontsize scales down for small nodes and up for big nodes
    base_font = max(6, min(12, int(math.sqrt(node_size) / 2.4)))

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


def draw_path(G, path, title="Path", fname="path.png"):
    """Draw full graph but emphasize a given path."""
    return draw_graph(G, title=title, node_size=1000, fname=fname, highlight_path=path)
