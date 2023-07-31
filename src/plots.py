import networkx as nx
import matplotlib.pyplot as plt
import querying


'''
Draws a directed graph of the first n dramas pointing to the k most similar other dramas.
'''
def draw_similarity_graph(n=100, k=3):
    all_dramas_query = "SELECT title, id FROM dramas"
    _, all_dramas = querying.query(all_dramas_query)

    print("Calculating similarities...")
    top_similars = {d[1]: querying.top_k_most_similar(d[1], k) for d in all_dramas[:n]}

    dramas = nx.DiGraph()

    # Add nodes
    for drama in all_dramas:
        dramas.add_node(drama[1], size=1)

    # Add edges from similarity dictionary
    for drama in top_similars:
        for e in top_similars[drama]:
            print(drama, e[1])
            dramas.add_edge(drama, e[1], weight=e[0])

    # Removing nodes with degree 0
    unused = []
    for node in dramas.nodes():
        if dramas.degree[node] == 0:
            unused.append(node)
    dramas.remove_nodes_from(unused)

    nx.draw(dramas)
    plt.show()
