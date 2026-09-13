"""Plotly figure for an educational B+ tree."""

import plotly.graph_objects as go

from .common import COLORS, base_figure, configure_3d, hide_axes


def bplus_tree_figure(root: object, mode: str = "3D", highlight: object | None = None) -> go.Figure:
    figure = base_figure("B+ Tree")
    levels: list[list[object]] = []
    pending = [root]
    while pending:
        levels.append(pending)
        next_level: list[object] = []
        for node in pending:
            next_level.extend(getattr(node, "children", []))
        pending = next_level
    positions: dict[int, tuple[float, float]] = {}
    for depth, nodes in enumerate(levels):
        for index, node in enumerate(nodes):
            positions[id(node)] = (index - (len(nodes) - 1) / 2, -depth)
    for nodes in levels:
        for node in nodes:
            for child in getattr(node, "children", []):
                x1, y1 = positions[id(node)]
                x2, y2 = positions[id(child)]
                trace_type = go.Scatter3d if mode == "3D" else go.Scatter
                kwargs = {"x": [x1, x2], "y": [y1, y2], "mode": "lines", "line": {"color": COLORS["edge"], "width": 5}}
                if mode == "3D":
                    kwargs["z"] = [0, 0]
                figure.add_trace(trace_type(**kwargs))
    for node in levels[-1] if levels else []:
        next_leaf = getattr(node, "next_leaf", None)
        if next_leaf is not None:
            x1, y1 = positions[id(node)]
            x2, y2 = positions[id(next_leaf)]
            figure.add_annotation(x=(x1 + x2) / 2, y=y1, text="⇢", showarrow=False, font={"color": COLORS["current"], "size": 18})
    nodes = [node for level in levels for node in level]
    trace_type = go.Scatter3d if mode == "3D" else go.Scatter
    kwargs = {"x": [positions[id(node)][0] for node in nodes], "y": [positions[id(node)][1] for node in nodes], "mode": "markers+text", "text": ["[" + ", ".join(map(str, getattr(node, "keys"))) + "]" for node in nodes], "textposition": "middle center", "marker": {"size": 22 if mode == "3D" else 64, "color": [COLORS["current"] if highlight in getattr(node, "keys") else COLORS["highlight"] if getattr(node, "is_leaf") else COLORS["node"] for node in nodes], "line": {"color": "#ffffff", "width": 2}}, "hovertemplate": "Keys: %{text}<extra></extra>"}
    if mode == "3D":
        kwargs["z"] = [0 for _ in nodes]
    figure.add_trace(trace_type(**kwargs))
    return configure_3d(figure) if mode == "3D" else hide_axes(figure)
