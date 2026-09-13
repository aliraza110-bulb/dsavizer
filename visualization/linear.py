"""Figures for queues, stacks, and linked lists."""

import plotly.graph_objects as go

from .common import COLORS, base_figure, configure_3d, hide_axes


def linear_figure(values: list[object], kind: str, highlight: object | None = None, mode: str = "3D") -> go.Figure:
    figure = base_figure(kind.title())
    if not values:
        name = "Queue" if kind == "queue" else "Stack" if kind == "stack" else kind.title()
        hint = "Enqueue an element to begin." if kind == "queue" else "Push an element to begin." if kind == "stack" else "Insert a node to begin."
        figure.add_annotation(text=f"{name} is empty<br><sup>{hint}</sup>", x=0.5, y=0.5, showarrow=False)
        return configure_3d(figure) if mode == "3D" else hide_axes(figure)
    if kind == "stack":
        x_values = [0] * len(values)
        y_values = list(range(len(values)))
        labels = [str(value) for value in values]
        trace_type = go.Scatter3d if mode == "3D" else go.Scatter
        trace_kwargs = {"x": x_values, "y": y_values, "mode": "markers+text", "text": labels, "textposition": "middle center"}
        if mode == "3D":
            trace_kwargs["z"] = [0.25] * len(values)
        trace_kwargs.update(
            marker={"size": 18 if mode == "3D" else 54, "color": [
                COLORS["highlight"] if value == highlight else COLORS["node"]
                for value in values
            ], "line": {"color": "#ffffff", "width": 2}},
            hovertemplate="Value: %{text}<extra></extra>",
        )
        figure.add_trace(trace_type(**trace_kwargs))
        if mode == "3D":
            figure.add_trace(go.Scatter3d(
                x=[-0.45, 0.45], y=[-0.45, 0.45], z=[0, 0], mode="lines",
                line={"color": COLORS["edge"], "width": 8}, hoverinfo="skip",
            ))
        figure.add_annotation(x=0, y=len(values), text="TOP", showarrow=False)
    else:
        x_values = list(range(len(values)))
        labels = [str(value) for value in values]
        trace_type = go.Scatter3d if mode == "3D" else go.Scatter
        trace_kwargs = {"x": x_values, "y": [0] * len(values), "mode": "markers+text", "text": labels, "textposition": "middle center"}
        if mode == "3D":
            trace_kwargs["z"] = [0.25] * len(values)
        trace_kwargs.update(marker={"size": 18 if mode == "3D" else 54, "color": [COLORS["highlight"] if value == highlight else COLORS["node"] for value in values], "line": {"color": "#ffffff", "width": 2}}, hovertemplate="Value: %{text}<extra></extra>")
        figure.add_trace(trace_type(**trace_kwargs))
        if kind == "queue":
            if len(values) == 1:
                figure.add_annotation(x=0, y=0.9, text="FRONT", showarrow=False)
                figure.add_annotation(x=0, y=0.55, text="REAR", showarrow=False)
            else:
                figure.add_annotation(x=0, y=0.65, text="FRONT", showarrow=False)
                figure.add_annotation(x=len(values) - 1, y=0.65, text="REAR", showarrow=False)
        else:
            for index in range(len(values) - 1):
                figure.add_annotation(
                    x=index + 0.5,
                    y=0,
                    ax=index + 0.25,
                    ay=0,
                    text="→",
                    showarrow=False,
                    font={"size": 20, "color": COLORS["edge"]},
                )
    return configure_3d(figure) if mode == "3D" else hide_axes(figure)


def linked_list_figure(values: list[object], doubly: bool = False, highlight: object | None = None, mode: str = "3D") -> go.Figure:
    figure = linear_figure(values, "doubly linked list" if doubly else "singly linked list", highlight, mode)
    if values:
        for index in range(len(values) - 1):
            figure.add_annotation(
                x=index + 0.5,
                y=0,
                text="⇄" if doubly else "→",
                showarrow=False,
                font={"size": 20, "color": COLORS["edge"]},
            )
        figure.add_annotation(x=len(values), y=0, text="NULL", showarrow=False)
    return figure
