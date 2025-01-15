import networkx as nx
import matplotlib.pyplot as plt

def visualize_and_export_graph(graph, edge_weight_tuples, top_n=None, output_path='channel_collaborations.dot'):
    """
    Visualizes the strongest relationships in the graph and exports to a DOT file.

    Parameters:
    - graph (networkx.Graph): The input graph.
    - edge_weight_tuples (list): List of (u, v, weight) tuples for graph edges.
    - top_n (int, optional): Number of top edges to include. If None, includes all edges.
    - output_path (str): Path to save the DOT file.
    """
    # Filter edges for the top N strongest relationships
    if top_n:
        top_edges = sorted(edge_weight_tuples, key=lambda x: x[2], reverse=True)[:top_n]
    else:
        top_edges = edge_weight_tuples

    # Create a subgraph containing the filtered edges
    subgraph = nx.Graph()
    subgraph.add_weighted_edges_from(top_edges)

    # Visualize the graph
    plt.figure(figsize=(20, 20))  # Adjust figure size
    pos = nx.spring_layout(subgraph, seed=42, k=0.3, iterations=50)  # Layout settings

    # Extract weights for visualization
    weights = [subgraph[u][v]['weight'] for u, v in subgraph.edges()]
    colors = [weight / max(weights) for weight in weights] if weights else []

    # Draw nodes and edges
    nx.draw_networkx_nodes(subgraph, pos, node_size=800, node_color='skyblue', edgecolors='black')
    nx.draw_networkx_edges(
        subgraph,
        pos,
        edgelist=subgraph.edges(),
        width=2,
        edge_color=colors,
        edge_cmap=plt.cm.plasma,
        alpha=0.8
    )
    nx.draw_networkx_labels(subgraph, pos, font_size=8, font_weight="bold",
                            bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=0.3'))

    # Add a color bar if weights exist
    if weights:
        sm = plt.cm.ScalarMappable(cmap=plt.cm.plasma, norm=plt.Normalize(vmin=min(weights), vmax=max(weights)))
        sm.set_array([])
        plt.colorbar(sm, label="Connection Strength", orientation="vertical", pad=0.02)

    # Add a title and show the plot
    title = f"Top {top_n} Strongest Relationships in Channel Collaborations" if top_n else "All Channel Collaborations"
    plt.title(title, fontsize=20)
    plt.show()

    # Export the graph to a DOT file
    nx.nx_agraph.write_dot(subgraph, output_path)
    print(f"DOT file saved to: {output_path}")

# Example usage
output_dot_file_path = '/mnt/data/top_channel_collaborations.dot'
visualize_and_export_graph(simplified_graph, edge_weight_tuples, top_n=200, output_path=output_dot_file_path)
