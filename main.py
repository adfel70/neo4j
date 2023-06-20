import networkx as nx
import matplotlib.pyplot as plt
from neo4j import GraphDatabase

uri = "bolt://localhost:7687"  # replace with your Neo4j instance
driver = GraphDatabase.driver(uri, auth = ("neo4j", "adamfel7070"))  # replace with your credentials


def get_data(driver):
    with driver.session() as session:
        results = session.run("""
            MATCH (person:Person)-[relatedTo]->(movie:Movie)
            RETURN person.name, TYPE(relatedTo), movie.title
        """)

        # Convert the result to a list so we can iterate over it multiple times
        results = list(results)

    return results


def create_graph(data):
    G = nx.Graph()

    for record in data:
        person = record["person.name"]
        movie = record["movie.title"]
        relationship = record["TYPE(relatedTo)"]

        G.add_node(person, label = "Person")
        G.add_node(movie, label = "Movie")
        G.add_edge(person, movie, label = relationship)

    return G


def visualize_graph(G):
    pos = nx.spring_layout(G)
    labels = {node: node for node in G.nodes()}

    plt.figure(figsize = (10, 10))
    nx.draw(G, pos, labels = labels, with_labels = True)
    plt.show()


data = get_data(driver)
G = create_graph(data)
visualize_graph(G)
