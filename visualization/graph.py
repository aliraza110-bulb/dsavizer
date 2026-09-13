"""Plotly figure for an undirected graph."""

import math

import plotly.graph_objects as go

from .common import COLORS, base_figure, configure_3d, hide_axes


def graph_figure(adjacency: dict[object, set[object]], visited: set[object] | None = None, mode: str = "3D") -> go.Figure:
    figure = base_figure("Undirected Graph")
    vertices = sorted(adjacency, key=str)
    if not vertices:
        figure.add_annotation(text="Graph is empty<br><sup>Add a vertex to begin.</sup>", x=0.5, y=0.5, showarrow=False)
        return configure_3d(figure) if mode == "3D" else hide_axes(figure)
    positions = {
        vertex: (math.cos(2 * math.pi * index / len(vertices)), math.sin(2 * math.pi * index / len(vertices)))
        for index, vertex in enumerate(vertices)
    }
    for vertex in vertices:
        for neighbor in adjacency[vertex]:
            if str(vertex) < str(neighbor):
                trace_type = go.Scatter3d if mode == "3D" else go.Scatter
                kwargs = {"x": [positions[vertex][0], positions[neighbor][0]], "y": [positions[vertex][1], positions[neighbor][1]], "mode": "lines", "line": {"color": COLORS["edge"], "width": 5}}
                if mode == "3D":
                    kwargs["z"] = [0, 0]
                figure.add_trace(trace_type(**kwargs))
    visited = visited or set()
    trace_type = go.Scatter3d if mode == "3D" else go.Scatter
    kwargs = {"x": [positions[vertex][0] for vertex in vertices], "y": [positions[vertex][1] for vertex in vertices], "mode": "markers+text", "text": [str(vertex) for vertex in vertices], "textposition": "middle center", "marker": {"size": 18 if mode == "3D" else 48, "color": [COLORS["visited"] if vertex in visited else COLORS["node"] for vertex in vertices], "line": {"color": "#ffffff", "width": 2}}, "hovertemplate": "Vertex: %{text}<extra></extra>"}
    if mode == "3D":
        kwargs["z"] = [0.15 * math.sin(index) for index in range(len(vertices))]
    figure.add_trace(trace_type(**kwargs))
    return configure_3d(figure) if mode == "3D" else hide_axes(figure)
