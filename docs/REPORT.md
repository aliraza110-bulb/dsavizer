# Data Structures Visualizer Report

## Abstract

Data Structures Visualizer is an educational Python application that exposes common data structures through one Dash dashboard. Users select a structure, perform operations, inspect a Plotly representation, and read operation-specific complexity information. The algorithm classes are independent from Dash so they can be tested directly.

## Implemented Scope

The current implementation includes Queue, Stack, Singly Linked List, Doubly Linked List, General Tree, Binary Search Tree, AVL Tree, B+ Tree, undirected Graph, and a linear-probing Hash Table. The dashboard supports operation controls, reset, readable random data, operation history, complexity metadata, and step-by-step traversal navigation.

B+ tree deletion, directed graphs, persistence, automatic playback, and AI explanations are future enhancements, not implemented features.

## Architecture

- `data_structures/`: framework-independent algorithms and node representations.
- `visualization/`: Plotly figures appropriate to each structure.
- `ui/`: Dash layout, callback state serialization, operation dispatch, and complexity metadata.
- `tests/`: pytest behavior and invariant tests.
- `app.py`: small Dash entry point exposing `app` and `server`.

Dash stores JSON-compatible snapshots in `dcc.Store`. Callbacks rebuild a structure, call its public methods, serialize the result, and ask a visualizer for a figure. Expected domain errors become status messages rather than crashing the page.

## Representation Choices

The general tree uses first-child/next-sibling links. Its preorder, postorder, and level-order traversals are standard; inorder is explicitly defined as inorder over the equivalent left-child/right-sibling binary projection. The AVL tree stores node heights and performs genuine LL, RR, LR, and RL rotations. The B+ tree uses order 4 by default, stores keys in leaves, splits full nodes, and links leaves for ordered traversal. The graph uses an undirected adjacency dictionary. The hash table uses open addressing with linear probing and tombstones.

## Testing

Run:

```text
python -m pip install -r requirements.txt
python -m pytest -q
```

The verified suite covers normal operations, empty structures, duplicates, missing values, invalid positions, AVL balancing and rotations, B+ tree splitting and linked leaves, graph traversal/mutation, and hash collisions/tombstones. Dashboard imports and empty-state figure rendering are also smoke-tested locally.

## Complexity Summary

Queue enqueue is O(1), while dequeue is O(n) because the educational list representation shifts remaining items. Stack push/pop/peek are O(1) amortized. Linked-list positional operations are O(n). An ordinary BST is O(log n) on average and O(n) in the worst case. AVL search, insert, and delete are O(log n). B+ tree search and insert are O(log n), and leaf traversal is O(n). BFS and DFS are O(V + E). Hash-table operations are O(1) on average and O(n) in the worst case.

## Deployment

The repository includes `Procfile` with `gunicorn app:server`. Deployment is planned for an approved platform after the local app is tested in the target environment. No live URL is claimed until an online deployment has actually been completed and verified.

## Limitations and Future Work

The project is an educational in-memory visualizer, not a production database or multi-user service. Future work may add B+ tree deletion, directed graphs, automatic traversal playback, richer accessibility checks, persistent sessions, and additional data structures.
