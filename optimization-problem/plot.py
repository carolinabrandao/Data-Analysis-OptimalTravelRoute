import matplotlib.pyplot as plt
import networkx as nx

def plot_route_with_labels(edges, start_node, end_node, node_labels):
    """
    Plots a graph with labeled nodes and highlights the route.
    
    Parameters:
    - edges: List of edges (i, j)
    - start_node: Starting node
    - end_node: Ending node
    - node_labels: Dictionary {node: label} with labels for each node
    """
    # Create a graph from the edges
    graph = nx.Graph()
    graph.add_edges_from(edges)

    # Find a route using BFS
    try:
        route = nx.shortest_path(graph, source=start_node, target=end_node)
    except nx.NetworkXNoPath:
        print("No path exists between the given nodes.")
        return
    
    # Plot the graph
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(graph)  # Positions for all nodes
    
    # Draw the graph
    nx.draw(graph, pos, with_labels=True, node_color="lightblue", edge_color="gray", node_size=800, font_size=10)
    
    # Highlight the route
    route_edges = list(zip(route, route[1:]))
    nx.draw_networkx_edges(graph, pos, edgelist=route_edges, edge_color="red", width=2)
    nx.draw_networkx_nodes(graph, pos, nodelist=route, node_color="orange", node_size=800)
    
    # Add node labels with an offset
    offset_pos = {node: (x, y + 0.05) for node, (x, y) in pos.items()}
    custom_labels = {node: f"{node_labels.get(node, '')}" for node in graph.nodes}
    nx.draw_networkx_labels(graph, offset_pos, labels=custom_labels, font_size=10, font_color="black")
    
    plt.title(f"Route from {start_node} to {end_node}")
    plt.show()

# Example usage:
edges = [(1, 2), (2, 3), (3, 4), (4, 5), (1, 6), (6, 5)]
node_labels = {
    1: "Start",
    2: "A",
    3: "B",
    4: "C",
    5: "Destination",
    6: "X"
}
