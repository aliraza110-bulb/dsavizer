"""Undirected graph with BFS and DFS traversals."""

from collections import deque
from typing import Hashable, TypeVar


Vertex = TypeVar("Vertex", bound=Hashable)


class Graph:
    """Undirected graph represented by adjacency sets."""

    def __init__(self) -> None:
        self.adjacency: dict[Vertex, set[Vertex]] = {}

    def add_vertex(self, vertex: Vertex) -> None:
        self.adjacency.setdefault(vertex, set())

    def add_edge(self, first: Vertex, second: Vertex) -> None:
        if first == second:
            raise ValueError("Self-loops are not supported.")
        self.add_vertex(first)
        self.add_vertex(second)
        self.adjacency[first].add(second)
        self.adjacency[second].add(first)

    def delete_vertex(self, vertex: Vertex) -> None:
        if vertex not in self.adjacency:
            raise KeyError(f"Vertex {vertex!r} was not found.")
        for neighbor in self.adjacency[vertex]:
            self.adjacency[neighbor].remove(vertex)
        del self.adjacency[vertex]

    def delete_edge(self, first: Vertex, second: Vertex) -> None:
        if first not in self.adjacency or second not in self.adjacency[first]:
            raise KeyError("Edge was not found.")
        self.adjacency[first].remove(second)
        self.adjacency[second].remove(first)

    def neighbors(self, vertex: Vertex) -> list[Vertex]:
        if vertex not in self.adjacency:
            raise KeyError(f"Vertex {vertex!r} was not found.")
        return sorted(self.adjacency[vertex], key=str)

    def bfs(self, start: Vertex) -> list[Vertex]:
        self._validate_start(start)
        visited = {start}
        order: list[Vertex] = []
        pending: deque[Vertex] = deque([start])
        while pending:
            vertex = pending.popleft()
            order.append(vertex)
            for neighbor in self.neighbors(vertex):
                if neighbor not in visited:
                    visited.add(neighbor)
                    pending.append(neighbor)
        return order

    def dfs(self, start: Vertex) -> list[Vertex]:
        self._validate_start(start)
        visited: set[Vertex] = set()
        order: list[Vertex] = []

        def visit(vertex: Vertex) -> None:
            visited.add(vertex)
            order.append(vertex)
            for neighbor in self.neighbors(vertex):
                if neighbor not in visited:
                    visit(neighbor)

        visit(start)
        return order

    def clear(self) -> None:
        self.adjacency.clear()

    def _validate_start(self, start: Vertex) -> None:
        if start not in self.adjacency:
            raise KeyError(f"Vertex {start!r} was not found.")
