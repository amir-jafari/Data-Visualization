"""
Network diagrams -- when the relationships ARE the data.

A network is nodes joined by edges. The trap is that the picture has no
natural coordinates: the layout algorithm invents positions, and different
algorithms give completely different-looking pictures of identical data. So
position means nothing unless you say what it means.

What it shows:
    * the same graph under four layouts, to prove position is arbitrary
    * encoding something real in size and colour (degree, community)
    * when a network diagram beats a table, and when it does not

Run it:
    python viz/basics/networks/networkx_basics.py
"""

import sys
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save                              # noqa: E402

# A small social graph with two obvious communities and one bridge between.
graph = nx.karate_club_graph()

# --- 1. position is arbitrary ----------------------------------------------
layouts = {
    "spring": nx.spring_layout(graph, seed=42),
    "circular": nx.circular_layout(graph),
    "kamada-kawai": nx.kamada_kawai_layout(graph),
    "random": nx.random_layout(graph, seed=42),
}

fig, axes = plt.subplots(1, 4, figsize=(15, 4))
for ax, (name, pos) in zip(axes, layouts.items()):
    nx.draw_networkx_edges(graph, pos, ax=ax, alpha=0.3, width=0.8)
    nx.draw_networkx_nodes(graph, pos, ax=ax, node_size=60, node_color="#4C72B0")
    ax.set_title(name, fontsize=11)
    ax.axis("off")

fig.suptitle("Identical graph, four layouts. Position carries NO meaning "
             "unless you give it some.", fontsize=12)
fig.tight_layout()
save(fig, __file__, "layouts-differ")

# --- 2. encode something real ----------------------------------------------
pos = nx.spring_layout(graph, seed=42)
degrees = dict(graph.degree())
communities = nx.community.greedy_modularity_communities(graph)
community_of = {node: i for i, group in enumerate(communities) for node in group}

fig, (left, right) = plt.subplots(1, 2, figsize=(13, 5.5))

nx.draw_networkx_edges(graph, pos, ax=left, alpha=0.25, width=0.8)
nx.draw_networkx_nodes(graph, pos, ax=left, node_size=80, node_color="#4C72B0")
left.set_title("Everything the same size and colour:\nonly the shape says anything",
               fontsize=10)
left.axis("off")

nx.draw_networkx_edges(graph, pos, ax=right, alpha=0.25, width=0.8)
nodes = nx.draw_networkx_nodes(
    graph, pos, ax=right,
    node_size=[degrees[n] * 45 for n in graph.nodes()],   # size = connections
    node_color=[community_of[n] for n in graph.nodes()],  # colour = community
    cmap="Set2",
)
# Label only the hubs -- labelling all 34 would be unreadable.
hubs = {n: n for n in graph.nodes() if degrees[n] >= 10}
nx.draw_networkx_labels(graph, pos, labels=hubs, ax=right, font_size=9,
                        font_weight="bold")
right.set_title("size = number of connections, colour = community,\n"
                "labels = the hubs only", fontsize=10)
right.axis("off")

fig.suptitle("Zachary's karate club, 34 members", fontsize=13)
fig.tight_layout()
save(fig, __file__, "encode-meaning")

# --- 3. when a network diagram is the wrong choice -------------------------
top = sorted(degrees.items(), key=lambda kv: -kv[1])[:10]

fig, (left, right) = plt.subplots(1, 2, figsize=(12, 4))

nx.draw_networkx_edges(graph, pos, ax=left, alpha=0.25, width=0.8)
nx.draw_networkx_nodes(graph, pos, ax=left, node_size=60, node_color="#CCCCCC")
left.set_title("'Who is most connected?' -- hard to read here", fontsize=10)
left.axis("off")

names = [f"member {n}" for n, _ in reversed(top)]
right.barh(names, [d for _, d in reversed(top)], color="#4C72B0")
right.set_xlabel("connections")
right.set_title("The same question, as a sorted bar chart", fontsize=10)

fig.suptitle("Networks are for STRUCTURE. For ranking a property, use a bar chart.",
             fontsize=12)
fig.tight_layout()
save(fig, __file__, "not-always-a-network")

print(f"""
  Graph: {graph.number_of_nodes()} nodes, {graph.number_of_edges()} edges,
  {len(communities)} communities found.

  Rules:
    layout position is arbitrary -- never say "X is near Y, so..."
    encode real quantities in size and colour, not decoration
    label the hubs, not everything
    "who is biggest/most connected?" is a BAR CHART question
""")
