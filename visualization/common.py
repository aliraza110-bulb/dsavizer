"""Shared Plotly styling helpers."""

import plotly.graph_objects as go


COLORS = {
    "node": "#2f6690",
    "highlight": "#2a9d8f",
    "current": "#f4a261",
    "error": "#e76f51",
    "visited": "#52b788",
    "edge": "#8d99ae",
    "text": "#1f2933",
}


def base_figure(title: str) -> go.Figure:
    figure = go.Figure()
    figure.update_layout(
        title=title,
        template="plotly_white",
        paper_bgcolor="#f8fafc",
        plot_bgcolor="#f8fafc",
        font={"family": "Georgia, serif", "color": COLORS["text"]},
        margin={"l": 24, "r": 24, "t": 64, "b": 24},
        showlegend=False,
        hovermode="closest",
        transition={"duration": 500, "easing": "cubic-in-out"},
        uirevision="dsa-visualizer",
    )
    return figure


def hide_axes(figure: go.Figure) -> go.Figure:
    figure.update_xaxes(visible=False)
    figure.update_yaxes(visible=False, scaleanchor="x", scaleratio=1)
    return figure


def configure_3d(figure: go.Figure) -> go.Figure:
    figure.update_layout(
        scene={
            "xaxis": {"visible": False},
            "yaxis": {"visible": False},
            "zaxis": {"visible": False},
            "aspectmode": "auto",
            "camera": {"eye": {"x": 1.45, "y": 1.45, "z": 1.1}},
        },
    )
    return figure
