# app.py
"""
Interactive CLI to test loading the CSV, running BFS/DFS, shortest paths, and MST.
Usage: python app.py
"""

from graph_module import load_csv_to_df, build_graph_from_df
from pathfinder import bfs_traversal, dfs_traversal, dijkstra_shortest_path, bellman_ford_shortest_path
from mst import build_mst
from visualize import draw_graph, draw_path

def main_menu():
    print("Travel Route Finder - simple CLI")
    print("1. Load graph and show basic info")
    print("2. BFS traversal from a city")
    print("3. DFS traversal from a city")
    print("4. Shortest path (Dijkstra)")
    print("5. Shortest path (Bellman-Ford)")
    print("6. Build MST (Tour Planner)")
    print("7. Draw full graph (visual)")
    print("8. Exit")

def run():
    df = load_csv_to_df()
    G = build_graph_from_df(df)
    while True:
        main_menu()
        choice = input("Choose (1-8): ").strip()
        if choice == "1":
            print("Nodes:", len(G.nodes()))
            print("Edges:", len(G.edges()))
            print("Sample nodes:", list(G.nodes())[:10])
        elif choice == "2":
            city = input("Start city: ").strip()
            if city not in G:
                print("City not in graph.")
                continue
            order = bfs_traversal(G, city)
            print("BFS order (first 50 shown):", order[:50])
        elif choice == "3":
            city = input("Start city: ").strip()
            if city not in G:
                print("City not in graph.")
                continue
            order = dfs_traversal(G, city)
            print("DFS order (first 50 shown):", order[:50])
        elif choice == "4":
            s = input("Source city: ").strip()
            t = input("Target city: ").strip()
            if s not in G or t not in G:
                print("One of the cities is not in graph.")
                continue
            dist, path = dijkstra_shortest_path(G, s, t)
            if path:
                print(f"Dijkstra: distance {dist:.0f} km, path: {path}")
                draw_path(G, path, title=f"Dijkstra: {s} -> {t} ({int(dist)} km)")
            else:
                print("No path found.")
        elif choice == "5":
            s = input("Source city: ").strip()
            t = input("Target city: ").strip()
            if s not in G or t not in G:
                print("One of the cities is not in graph.")
                continue
            dist, path = bellman_ford_shortest_path(G, s, t)
            if path:
                print(f"Bellman-Ford: distance {dist:.0f} km, path: {path}")
                draw_path(G, path, title=f"Bellman-Ford: {s} -> {t} ({int(dist)} km)")
            else:
                print("No path found.")
        elif choice == "6":
            T, w = build_mst(G)
            print("MST built. Edges:", len(T.edges()), "Total distance:", int(w))
            draw_graph(T, title=f"MST (Total {int(w)} km)", node_size=60)
        elif choice == "7":
            draw_graph(G, title="Full City Graph", node_size=200)
        elif choice == "8":
            print("Bye!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    run()

