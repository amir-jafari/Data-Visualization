"""
PyVis -- a network you can drag, for when the static picture is too dense.

Past roughly fifty nodes a static network diagram becomes a hairball. An
interactive one lets the reader pull nodes apart and follow a single thread,
which is the one job static cannot do.

What it shows:
    * turning a networkx graph into an interactive HTML page
    * carrying real information in size, colour and hover text
    * physics settings, which decide whether it settles or wobbles forever

Run it:
    python viz/basics/networks/pyvis_interactive.py
    then open the .html file it prints and drag a node

In Streamlit, read the HTML and pass it to st.components.v1.html(...) --
the same trick fastapi/project/client.py uses for folium maps.
"""

import sys
from pathlib import Path

import networkx as nx
from pyvis.network import Network

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
from vizkit import save_html                         # noqa: E402

graph = nx.karate_club_graph()
degrees = dict(graph.degree())
communities = nx.community.greedy_modularity_communities(graph)
community_of = {node: i for i, group in enumerate(communities) for node in group}
palette = ["#0072B2", "#E69F00", "#009E73", "#CC79A7", "#56B4E9"]

network = Network(height="620px", width="100%", bgcolor="#ffffff",
                  font_color="#333333", notebook=False, cdn_resources="in_line")

for node in graph.nodes():
    network.add_node(
        node,
        label=str(node),
        # Same encodings as the static lesson: size = connections, colour = group.
        size=8 + degrees[node] * 1.6,
        color=palette[community_of[node] % len(palette)],
        # Hover text can hold what the picture has no room for.
        title=f"member {node}\nconnections: {degrees[node]}\n"
              f"community: {community_of[node]}",
    )

for source, target in graph.edges():
    network.add_edge(source, target, color="#DDDDDD")

# Physics decides whether the layout settles. Too little damping and it never
# stops moving, which is nauseating to read.
network.barnes_hut(gravity=-4000, central_gravity=0.3, spring_length=110,
                   spring_strength=0.02, damping=0.9)

save_html(network, __file__, "karate-club")

print("""
  Interactive networks are worth it above ~50 nodes, where a static picture
  turns into a hairball. Below that, the static version prints and pastes.

  Same encodings either way: size = a quantity, colour = a group,
  hover = the detail there is no room for.
""")
