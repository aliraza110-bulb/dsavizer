# Data Structures Visualizer

An academic Dash and Plotly project for interactively learning how common data
structures work. Development is being completed in small, testable phases.

## Current Status

The implemented application includes:

- Queue with FIFO operations
- Stack with LIFO operations
- Singly linked list with positional insertion/deletion and search
- Doubly linked list with forward and backward traversal
- General tree, BST, AVL tree, educational B+ tree, undirected graph, and linear-probing hash table
- Plotly visualizations and a unified Dash dashboard
- Reset, readable random data, operation history, complexity information, and traversal step controls
- Automated tests for all data structures

The project remains an educational in-memory visualizer. B+ tree deletion,
directed graphs, automatic playback, persistence, and AI explanations are
planned enhancements and are not claimed as implemented. See
[docs/PHASE_1_PLAN.md](docs/PHASE_1_PLAN.md) for the architecture and roadmap.

## Run Tests

Install the dependencies and run the current suite:

```text
python -m pip install -r requirements.txt
python -m pytest -q
```

Start the dashboard locally with:

```text
python app.py
```

Then open `http://127.0.0.1:8050`.

## Documentation

- [Implementation report](docs/REPORT.md)
- [Viva notes](docs/VIVA_NOTES.md)
- [Phase 1 architecture plan](docs/PHASE_1_PLAN.md)

## Deployment

`Procfile` contains the production command `gunicorn app:server`. A live URL
will be added only after deployment and online verification.