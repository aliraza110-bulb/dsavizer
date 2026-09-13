"""Entry point for the Data Structures Visualizer Dash application."""

from dash import Dash

from ui.callbacks import register_callbacks
from ui.layout import dashboard_layout


app = Dash(__name__, title="Data Structures Visualizer")
app.layout = dashboard_layout()
register_callbacks(app)
server = app.server


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8050)
