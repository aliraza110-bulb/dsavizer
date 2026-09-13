"""Dashboard layout and control metadata."""

from dash import dcc, html

STRUCTURES = [
    "Queue", "Stack", "Singly Linked List", "Doubly Linked List", "General Tree",
    "Binary Search Tree", "AVL Tree", "B+ Tree", "Graph", "Hash Table",
]

OPERATIONS = {
    "Queue": ["Enqueue", "Dequeue", "Peek", "Display"],
    "Stack": ["Push", "Pop", "Peek", "Display"],
    "Singly Linked List": ["Insert Beginning", "Insert End", "Insert Position", "Delete", "Search", "Traverse"],
    "Doubly Linked List": ["Insert Beginning", "Insert End", "Insert Position", "Delete", "Search", "Forward Traversal", "Backward Traversal"],
    "General Tree": ["Create Root", "Add Child", "Delete Node", "Search", "Preorder", "Inorder", "Postorder", "Level Order"],
    "Binary Search Tree": ["Insert", "Search", "Delete", "Minimum", "Maximum", "Inorder", "Preorder", "Postorder", "Level Order"],
    "AVL Tree": ["Insert", "Search", "Delete", "Height", "Inorder", "Preorder", "Postorder", "Level Order"],
    "B+ Tree": ["Insert", "Search", "Leaf Traversal"],
    "Graph": ["Add Vertex", "Add Edge", "Delete Vertex", "Delete Edge", "BFS", "DFS"],
    "Hash Table": ["Insert", "Search", "Delete", "Display"],
}

DESCRIPTIONS = {
    "Queue": "FIFO data structure", "Stack": "LIFO data structure",
    "Singly Linked List": "Nodes with forward links", "Doubly Linked List": "Nodes with two-way links",
    "General Tree": "Parent-child hierarchy", "Binary Search Tree": "Ordered binary nodes",
    "AVL Tree": "Self-balancing BST", "B+ Tree": "Indexed linked leaves",
    "Graph": "Vertices and edges", "Hash Table": "Key-value storage",
}


def dashboard_layout() -> html.Div:
    structure_options = [
        {"label": html.Div([html.Strong(name), html.Span(DESCRIPTIONS[name])]), "value": name}
        for name in STRUCTURES
    ]
    return html.Div([
        dcc.Store(id="state-store", data={"structure": "Queue", "values": [], "history": [], "steps": [], "step_index": 0}),
        html.Header([
            html.Div([html.Div("DS", className="brand-mark"), html.Div([
                html.Div("Data Structures Visualizer", className="brand-name"),
                html.Div("Interactive algorithms laboratory", className="brand-kicker"),
            ])], className="brand"),
            html.Div([html.Span("●", className="ready-dot"), " Ready"], className="ready-status"),
        ], className="site-header"),
        html.Main([
            html.Section([
                html.P("DATA STRUCTURES", className="section-label"),
                html.H1("Explore how data moves, connects, and changes."),
                html.P("Select a structure to open its interactive laboratory.", className="page-intro"),
            ], className="intro-section"),
            html.Section([
                html.P("DATA STRUCTURES", className="section-label"),
                dcc.RadioItems(id="structure-selector", options=structure_options, value="Queue", className="structure-grid", labelClassName="structure-option", inputClassName="structure-radio"),
            ], className="selector-section"),
            html.Section([
                html.Div([
                    html.Div([html.P("LIVE VISUALIZATION", className="section-label"), html.H2("Structure canvas")], className="visual-heading"),
                    html.Div([
                        html.Span("VIEW", className="toolbar-label"),
                        dcc.RadioItems(id="view-mode", options=[{"label": "2D", "value": "2D"}, {"label": "3D", "value": "3D"}], value="3D", inline=True, className="view-mode"),
                    ], className="view-toolbar"),
                    html.Div(id="status-panel", className="status-panel"),
                ], className="canvas-top"),
                dcc.Graph(id="structure-graph", config={"displayModeBar": True, "displaylogo": False, "responsive": True, "modeBarButtonsToAdd": ["resetCameraDefault3d"]}, className="structure-graph"),
                html.Div([
                    html.Span("NODE STATES", className="legend-title"),
                    html.Span([html.I(className="legend-dot node-dot"), "Stored"], className="legend-item"),
                    html.Span([html.I(className="legend-dot active-dot"), "Current"], className="legend-item"),
                    html.Span([html.I(className="legend-dot visited-dot"), "Visited"], className="legend-item"),
                ], className="legend-row"),
                html.Div([
                    html.Span("OPERATIONS", className="toolbar-label"),
                    html.Div([html.Label("Value", id="value-label", htmlFor="value-input"), dcc.Input(id="value-input", type="text", placeholder="Enter value")], className="input-group compact-input"),
                    html.Div([html.Label("Position / second value", id="secondary-label", htmlFor="secondary-input"), dcc.Input(id="secondary-input", type="text", placeholder="Enter value")], className="input-group compact-input secondary-control"),
                    html.Div(id="operation-buttons", className="operation-list"),
                ], className="visual-operation-bar"),
            ], className="visual-card"),
            html.Section([
                html.Div([
                    html.P("OPERATIONS", className="section-label"),
                    html.H2("Work with the active structure"),
                ], className="operation-picker"),
                html.Div([
                    html.Div([
                        html.Button("Generate random data", id="random-button", n_clicks=0, className="secondary-button"),
                        html.Button("Reset", id="reset-button", n_clicks=0, className="reset-button"),
                    ], className="action-buttons"),
                ], className="control-form"),
            ], className="operations-card"),
            html.Section([
                html.Div([
                    html.Div([html.P("RESULT / STATUS", className="section-label"), html.H2("Latest activity")], className="result-heading"),
                    html.Div([html.H3("EXPLANATION", className="subheading"), html.Div(id="explanation-panel")], className="explanation-card"),
                    html.Div([html.H3("COMPLEXITY", className="subheading"), html.Div(id="complexity-panel")], className="complexity-card"),
                    html.Div([
                        html.Div([html.H3("TRAVERSAL", className="subheading"), html.Span("STEP MODE", className="mini-pill")], className="section-heading"),
                        html.Div(id="step-label", className="step-label"),
                        html.Div([html.Button("Previous", id="previous-button", n_clicks=0, className="step-button"), html.Button("Next", id="next-button", n_clicks=0, className="step-button")], className="step-actions"),
                    ], className="traversal-card"),
                    html.Div([html.H3("OPERATION HISTORY", className="subheading"), html.Ol(id="history-panel")], className="history-card"),
                ], className="details-grid"),
                html.Div([
                    html.Div([html.H3("ANIMATION", className="subheading"), html.Span("STEP THROUGH THE IDEA", className="mini-pill")], className="section-heading"),
                    html.Div([
                        html.Button("Play", id="animation-play", n_clicks=0, className="primary-button"),
                        html.Button("Pause", id="animation-pause", n_clicks=0, className="secondary-button"),
                        html.Button("Previous", id="animation-previous", n_clicks=0, className="step-button"),
                        html.Button("Next", id="animation-next", n_clicks=0, className="step-button"),
                        html.Label(["Speed", dcc.Slider(id="animation-speed", min=400, max=1800, step=100, value=900, marks=None, tooltip={"placement": "bottom", "always_visible": False})], className="speed-control"),
                    ], className="animation-actions"),
                ], id="animation-controls", className="animation-card", style={"display": "none"}),
            ], className="details-section"),
            dcc.Interval(id="animation-timer", interval=900, n_intervals=0, disabled=True),
        ]),
        html.Footer("Data Structures & Algorithms Laboratory", className="footer"),
    ])
