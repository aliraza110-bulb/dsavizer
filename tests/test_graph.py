import pytest

from data_structures.graph import Graph


def test_graph_bfs_and_dfs() -> None:
    graph = Graph()
    graph.add_edge(1, 2)
    graph.add_edge(1, 3)
    graph.add_edge(2, 4)

    assert graph.bfs(1) == [1, 2, 3, 4]
    assert graph.dfs(1) == [1, 2, 4, 3]


def test_graph_mutations_and_invalid_operations() -> None:
    graph = Graph()
    graph.add_edge("a", "b")
    graph.add_edge("b", "c")
    graph.delete_edge("a", "b")
    graph.delete_vertex("c")

    assert graph.neighbors("b") == []
    with pytest.raises(ValueError):
        graph.add_edge("b", "b")
    with pytest.raises(KeyError):
        graph.bfs("missing")
