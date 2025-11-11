# graph_module.py
"""
Load city_distances.csv and build a NetworkX weighted graph.
"""

import csv
import networkx as nx
import pandas as pd

CSV_FILE = "city_distances.csv"

def load_csv_to_df(csvfile=CSV_FILE):
    df = pd.read_csv(csvfile, index_col=0)
    # Ensure numeric
    df = df.apply(pd.to_numeric)
    return df

def build_graph_from_df(df):
    G = nx.Graph()
    for city in df.index:
        G.add_node(city)
    for i, a in enumerate(df.index):
        for j, b in enumerate(df.columns):
            if j <= i:  # undirected; avoid duplicates
                continue
            w = df.at[a, b]
            if w > 0:
                G.add_edge(a, b, weight=float(w))
    return G

def adjacency_matrix(G):
    return nx.to_pandas_adjacency(G, weight='weight')

def adjacency_list(G):
    return {n: list(G[n].items()) for n in G.nodes()}

if __name__ == "__main__":
    df = load_csv_to_df()
    G = build_graph_from_df(df)
    print("Nodes:", len(G.nodes()))
    print("Edges:", len(G.edges()))
    print("Sample edges (first 10):", list(G.edges(data=True))[:10])
