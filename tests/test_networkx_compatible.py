import json

import networkx as nx


def test_loading_to_networkx(node_link_path: str) -> None:
    with open(node_link_path) as f:
        data = json.load(f)
    graph = nx.node_link_graph(data=data, directed=True)
    gene_descendants = nx.ancestors(graph, "gene:AET2Gv20728000")
    assert len(gene_descendants) == 10

