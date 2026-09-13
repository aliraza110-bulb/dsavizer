"""Figures for general, binary-search, and AVL trees."""

import plotly.graph_objects as go

from .common import COLORS, base_figure, configure_3d, hide_axes


def binary_tree_figure(root: object | None, title: str, show_balance: bool = False, mode: str = "3D", highlight: object | None = None) -> go.Figure:
    figure = base_figure(title)
    if root is None:
        figure.add_annotation(text="Tree is empty<br><sup>Insert a value to create the root.</sup>", x=0.5, y=0.5, showarrow=False)
        return configure_3d(figure) if mode == "3D" else hide_axes(figure)
    positions: dict[int, tuple[float, float]] = {}
    edges: list[tuple[int, int]] = []
    counter = [0]

    def assign(node: object | None, depth: int) -> None:
        if node is None:
            return
        assign(getattr(node, "left"), depth + 1)
        positions[id(node)] = (counter[0], -depth)
        counter[0] += 1
        assign(getattr(node, "right"), depth + 1)
        for child_name in ("left", "right"):
            child = getattr(node, child_name)
            if child is not None:
                edges.append((id(node), id(child)))

    assign(root, 0)
    for parent_id, child_id in edges:
        x1, y1 = positions[parent_id]
        x2, y2 = positions[child_id]
        trace_type = go.Scatter3d if mode == "3D" else go.Scatter
        kwargs = {"x": [x1, x2], "y": [y1, y2], "mode": "lines", "line": {"color": COLORS["edge"], "width": 5}}
        if mode == "3D":
            kwargs["z"] = [0, 0]
        figure.add_trace(trace_type(**kwargs))
    labels = []
    colors = []
    for node_id, (x, y) in positions.items():
        labels.append(str(_node_label(root, node_id, show_balance)))
        colors.append(COLORS["current"] if _node_value(root, node_id) == highlight else COLORS["node"])
    trace_type = go.Scatter3d if mode == "3D" else go.Scatter
    kwargs = {"x": [position[0] for position in positions.values()], "y": [position[1] for position in positions.values()], "mode": "markers+text", "text": labels, "textposition": "middle center", "marker": {"size": 18 if mode == "3D" else 48, "color": colors, "line": {"color": "#ffffff", "width": 2}}, "hovertemplate": "Node: %{text}<extra></extra>"}
    if mode == "3D":
        kwargs["z"] = [0 for _ in positions]
    figure.add_trace(trace_type(**kwargs))
    return configure_3d(figure) if mode == "3D" else hide_axes(figure)


def _node_label(root: object, target_id: int, show_balance: bool) -> str:
    found: list[object] = []

    def visit(node: object | None) -> None:
        if node is None or found:
            return
        if id(node) == target_id:
            found.append(node)
            return
        visit(getattr(node, "left", None))
        visit(getattr(node, "right", None))

    visit(root)
    node = found[0]
    label = str(getattr(node, "value"))
    if show_balance:
        left = getattr(getattr(node, "left", None), "height", 0)
        right = getattr(getattr(node, "right", None), "height", 0)
        label = f"{label}\nBF={left - right}"
    return label


def _node_value(root: object, target_id: int) -> object:
    found: list[object] = []

    def visit(node: object | None) -> None:
        if node is None or found:
            return
        if id(node) == target_id:
            found.append(node)
            return
        visit(getattr(node, "left", None))
        visit(getattr(node, "right", None))

    visit(root)
    return getattr(found[0], "value", None)


def general_tree_figure(root: object | None, mode: str = "3D", highlight: object | None = None) -> go.Figure:
    figure = base_figure("General Tree")
    if root is None:
        figure.add_annotation(text="Tree is empty<br><sup>Add a node to begin.</sup>", x=0.5, y=0.5, showarrow=False)
        return configure_3d(figure) if mode == "3D" else hide_axes(figure)
    positions: dict[int, tuple[float, float]] = {}
    edges: list[tuple[int, int]] = []
    counter = [0]

    def assign(node: object | None, depth: int) -> None:
        if node is None:
            return
        child = getattr(node, "first_child")
        child_ids: list[int] = []
        while child is not None:
            assign(child, depth + 1)
            child_ids.append(id(child))
            child = getattr(child, "next_sibling")
        if child_ids:
            x = sum(positions[child_id][0] for child_id in child_ids) / len(child_ids)
            for child_id in child_ids:
                edges.append((id(node), child_id))
        else:
            x = counter[0]
            counter[0] += 1
        positions[id(node)] = (x, -depth)

    assign(root, 0)
    for parent_id, child_id in edges:
        x1, y1 = positions[parent_id]
        x2, y2 = positions[child_id]
        trace_type = go.Scatter3d if mode == "3D" else go.Scatter
        kwargs = {"x": [x1, x2], "y": [y1, y2], "mode": "lines", "line": {"color": COLORS["edge"], "width": 5}}
        if mode == "3D":
            kwargs["z"] = [0, 0]
        figure.add_trace(trace_type(**kwargs))
    labels = {}
    def collect(node: object | None) -> None:
        if node is None:
            return
        labels[id(node)] = str(getattr(node, "value"))
        collect(getattr(node, "first_child"))
        collect(getattr(node, "next_sibling"))
    collect(root)
    trace_type = go.Scatter3d if mode == "3D" else go.Scatter
    kwargs = {"x": [position[0] for position in positions.values()], "y": [position[1] for position in positions.values()], "mode": "markers+text", "text": [labels[node_id] for node_id in positions], "textposition": "middle center", "marker": {"size": 18 if mode == "3D" else 48, "color": [COLORS["current"] if labels[node_id] == str(highlight) else COLORS["node"] for node_id in positions], "line": {"color": "#ffffff", "width": 2}}, "hovertemplate": "Node: %{text}<extra></extra>"}
    if mode == "3D":
        kwargs["z"] = [0 for _ in positions]
    figure.add_trace(trace_type(**kwargs))
    return configure_3d(figure) if mode == "3D" else hide_axes(figure)
