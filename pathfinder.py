# pathfinder.py
"""
Path finding utilities:
- BFS (unweighted traversal)
- DFS (traversal)
- Dijkstra (shortest path by weight)
- Bellman-Ford (handles negative weights; our distances are positive)
"""

import networkx as nx
from collections import deque

def bfs_traversal(G, start):
    visited = []
    q = deque([start])
    seen = {start}
    while q:
        u = q.popleft()
        visited.append(u)
        for v in G.neighbors(u):
            if v not in seen:
                seen.add(v)
                q.append(v)
    return visited

def dfs_traversal(G, start):
    visited = []
    def dfs(u):
        visited.append(u)
        for v in G.neighbors(u):
            if v not in visited:
                dfs(v)
    dfs(start)
    return visited

def dijkstra_shortest_path(G, source, target):
    try:
        length, path = nx.single_source_dijkstra(G, source, target, weight='weight')
        return length, path
    except nx.NetworkXNoPath:
        return float('inf'), []

def bellman_ford_shortest_path(G, source, target):
    try:
        length, path = nx.single_source_bellman_ford(G, source, target, weight='weight')
        return length, path
    except Exception as e:
        return float('inf'), []

# convenience wrapper to get all-pairs shortest path lengths (Dijkstra)
def all_pairs_shortest_paths(G):
    return dict(nx.all_pairs_dijkstra_path_length(G, weight='weight'))
