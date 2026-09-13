"""Plotly figure for hash-table slots."""

import plotly.graph_objects as go

from .common import COLORS, base_figure, configure_3d, hide_axes


def hash_table_figure(slots: list[object], mode: str = "3D", highlight: object | None = None) -> go.Figure:
    figure = base_figure("Hash Table: Linear Probing")
    if not slots:
        return configure_3d(figure) if mode == "3D" else hide_axes(figure)
    labels = ["-" if value is None else str(value) for value in slots]
    if mode == "3D":
        figure.add_trace(go.Scatter3d(
            x=list(range(len(slots))), y=[0] * len(slots), z=[0.2] * len(slots),
            mode="markers+text", text=labels, textposition="middle center",
            marker={"size": 18, "color": [COLORS["current"] if index == highlight else COLORS["highlight"] if value not in (None, "<deleted>") else COLORS["error"] if value == "<deleted>" else COLORS["node"] for index, value in enumerate(slots)], "line": {"color": "#ffffff", "width": 2}},
            customdata=list(range(len(slots))), hovertemplate="Index %{customdata}<br>Value: %{text}<extra></extra>",
        ))
        figure.add_annotation(text="Linear probing: check the next slot after a collision.", x=0.5, y=0.04, xref="paper", yref="paper", showarrow=False)
        return configure_3d(figure)
    figure.add_trace(go.Table(
        header={"values": ["Index"] + list(map(str, range(len(slots)))), "fill_color": "#264653", "font": {"color": "white"}},
        cells={"values": [["Value"] + labels], "fill_color": "#e9f5f2"},
    ))
    figure.update_layout(yaxis={"visible": False})
    return figure
