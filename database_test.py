import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

# === Load the graph ===
G = nx.read_edgelist("graph0/0.edges", nodetype=int)

# === Load node features (each row: node ID, rest are binary features) ===
features = {}
with open("graph0/0.feat") as f:
    for line in f:
        parts = line.strip().split()
        node = int(parts[0])
        feats = np.array(list(map(int, parts[1:])))
        features[node] = feats

# === Load ego feature vector ===
egofeat = np.loadtxt("graph0/0.egofeat").reshape(1, -1)

# === Load feature names (optional)
with open("graph0/0.featnames") as f:
    featnames = [line.strip().split()[-1] for line in f]

# === Assign features to graph nodes ===
for node in G.nodes():
    if node in features:
        G.nodes[node]['features'] = features[node]
    else:
        print(f"Warning: no features found for node {node}")

# === Add ego node (node 0) and connect to all other nodes ===
G.add_node(0)
G.nodes[0]['features'] = egofeat[0]
for node in G.nodes():
    if node != 0:
        G.add_edge(0, node)

# compute similarities as before
similarities = {node: cosine_similarity(egofeat,
                     G.nodes[node]['features'].reshape(1,-1))[0][0]
                for node in G.nodes()}

# prepare colors
node_colors = [similarities[n] for n in G.nodes()]

# plot
plt.figure(figsize=(10,10))
pos = nx.spring_layout(G, seed=42)

# draw nodes, capture the PathCollection
nodes = nx.draw_networkx_nodes(
    G, pos,
    node_color=node_colors,
    cmap=plt.cm.viridis,
    node_size=30
)
nx.draw_networkx_edges(G, pos, alpha=0.1)

plt.title("Ego Network of User 0 (Cosine Similarity)")
plt.axis('off')

# now pass that collection into colorbar
plt.colorbar(nodes, label='Cosine Similarity')

plt.show()