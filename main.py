"""
Shortest Route Finder Between Brazilian Cities
Using Dijkstra's Algorithm

Author: Gean Gontijo
Date: 2026-04-16
"""

import heapq
import networkx as nx
import matplotlib.pyplot as plt


# --- 1. DATA: Brazilian cities and distances (km) ---

# Each tuple is (city_a, city_b, distance_km)
EDGES = [
    ("Sao Paulo", "Rio de Janeiro", 430),
    ("Sao Paulo", "Belo Horizonte", 586),
    ("Sao Paulo", "Curitiba", 408),
    ("Rio de Janeiro", "Belo Horizonte", 434),
    ("Rio de Janeiro", "Vitoria", 521),
    ("Belo Horizonte", "Brasilia", 716),
    ("Belo Horizonte", "Vitoria", 524),
    ("Brasilia", "Goiania", 209),
    ("Brasilia", "Salvador", 1446),
    ("Curitiba", "Florianopolis", 300),
    ("Curitiba", "Porto Alegre", 711),
    ("Florianopolis", "Porto Alegre", 476),
    ("Goiania", "Cuiaba", 890),
    ("Salvador", "Recife", 839),
    ("Recife", "Fortaleza", 800),
    ("Fortaleza", "Belem", 1610),
    ("Belem", "Manaus", 5298),
    ("Goiania", "Sao Paulo", 926),
]


def build_graph(edges):
    """Build an adjacency list from the edge list.

    Returns a dict like:
        {"Sao Paulo": [("Rio de Janeiro", 430), ("Belo Horizonte", 586), ...], ...}
    """
    graph = {}
    for city_a, city_b, distance in edges:
        graph.setdefault(city_a, []).append((city_b, distance))
        graph.setdefault(city_b, []).append((city_a, distance))
    return graph


# --- 2. DIJKSTRA: Implement the algorithm here! ---

def dijkstra(graph, start, end):
    """Find the shortest path between `start` and `end` using Dijkstra's algorithm.

    Args:
        graph: adjacency list (dict of lists of (neighbor, weight) tuples)
        start: name of the starting city
        end:   name of the destination city

    Returns:
        (total_distance, path) where path is a list of city names from start to end.
        Returns (float('inf'), []) if no path exists.

    Hints:
        - Use a priority queue (min-heap) with heapq:
            heapq.heappush(heap, (distance, city))
            distance, city = heapq.heappop(heap)

        - Keep a dict `distances` mapping each city to its best known distance from start.
          Initialize start to 0, everything else to infinity.

        - Keep a dict `previous` mapping each city to the city that came before it
          on the shortest path. Use this to reconstruct the path at the end.

        - When you pop a city from the heap, skip it if you already found a better path.

        - For each neighbor of the current city, check if going through the current city
          is shorter than the best known distance. If yes, update and push to the heap.
    """

    # Initialize your data structures
    distances = {city: float('inf') for city in graph}
    distances[start] = 0

    previous = {}

    heap = [(0, start)]

    processed = set()

    # Main loop - process nodes from the priority queue
    while heap:
        distance, city = heapq.heappop(heap)

        if city in processed:
            continue

        if city == end:
            break

        processed.add(city)

        out_neighbors = graph[city]
        for neighbor, weight in out_neighbors:
            new_distance = distance + weight

            if distances[neighbor] > new_distance:
                distances[neighbor] = new_distance
                previous[neighbor] = city
                heapq.heappush(heap, (new_distance, neighbor))
                
    # Reconstruct the path from `previous`
    path = []
    city = end

    while city is not None:
        path.append(city)
        city = previous.get(city)

    path.reverse()
    
    if path[0] == start:
        return distances[end], path
    else:
        return float("inf"), []

# --- 3. VISUALIZATION ---

def visualize(graph, shortest_path=None):
    """Draw the city graph, highlighting the shortest path if provided."""
    G = nx.Graph()

    for city, neighbors in graph.items():
        for neighbor, dist in neighbors:
            G.add_edge(city, neighbor, weight=dist)

    pos = nx.spring_layout(G, seed=42, k=2)

    plt.figure(figsize=(14, 9))
    plt.title("Brazilian Cities - Shortest Route (Dijkstra)", fontsize=16)

    # Draw all edges in light gray
    nx.draw_networkx_edges(G, pos, edge_color="#cccccc", width=1.5)
    nx.draw_networkx_nodes(G, pos, node_color="#4a90d9", node_size=500)
    nx.draw_networkx_labels(G, pos, font_size=8, font_weight="bold")

    # Draw edge labels (distances)
    edge_labels = nx.get_edge_attributes(G, "weight")
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=6, font_color="#666666")

    # Highlight shortest path
    if shortest_path and len(shortest_path) > 1:
        path_edges = list(zip(shortest_path, shortest_path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="#e74c3c", width=3)
        nx.draw_networkx_nodes(G, pos, nodelist=shortest_path, node_color="#e74c3c", node_size=600)

    plt.tight_layout()
    plt.savefig("shortest_route.png", dpi=150)
    print("Graph saved to shortest_route.png")
    plt.show()


# --- 4. MAIN ---

def main():
    graph = build_graph(EDGES)

    print("=" * 50)
    print("  Dijkstra's Shortest Route Finder")
    print("  Brazilian Cities Edition")
    print("=" * 50)

    # Show available cities
    cities = sorted(graph.keys())
    print("\nAvailable cities:")
    for i, city in enumerate(cities, 1):
        print(f"  {i:2d}. {city}")

    # Get user input
    print()
    start = input("Origin city: ").strip()
    end = input("Destination city: ").strip()

    if start not in graph:
        print(f"Error: '{start}' not found. Type the city name exactly as listed.")
        return
    if end not in graph:
        print(f"Error: '{end}' not found. Type the city name exactly as listed.")
        return

    # Run Dijkstra
    distance, path = dijkstra(graph, start, end)

    if distance == float("inf"):
        print(f"\nNo route found between {start} and {end}.")
    else:
        print(f"\nShortest route from {start} to {end}:")
        print(f"  Path: {' -> '.join(path)}")
        print(f"  Total distance: {distance} km")

    # Visualize
    visualize(graph, path)


if __name__ == "__main__":
    main()
