# mst.py
"""
Build MST to act as a simple 'tour planner' — gives a minimum-connectivity route connecting all cities.
"""

import networkx as nx

def build_mst(G):
    # returns an MST graph (undirected)
    T = nx.minimum_spanning_tree(G, weight='weight', algorithm='kruskal')
    total_weight = sum(d['weight'] for u,v,d in T.edges(data=True))
    return T, total_weight

if __name__ == "__main__":
    # quick test (if run directly) - requires graph_module
    from graph_module import load_csv_to_df, build_graph_from_df
    df = load_csv_to_df()
    G = build_graph_from_df(df)
    T, w = build_mst(G)
    print("MST edges:", len(T.edges()), "Total weight:", w)
