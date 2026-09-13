# Data Structures Visualizer
## Phase 1: Planning Specification

**Status:** Architecture approved; implementation completed through local validation
**Date:** 2026-09-13
**Implementation status:** Core structures, Plotly visualizers, Dash dashboard, tests, and local deployment configuration are implemented. Online deployment remains pending.

## 1. Project Goal

Build one Dash dashboard that lets a user select a data structure, perform an operation, inspect the updated structure in a Plotly visualization, and read the operation result and complexity. The implementation will prioritize correctness, explainability, and testability over production-scale performance.

The data-structure classes will be framework-independent. Dash callbacks will translate user actions into method calls and will render returned state; they will not contain algorithm implementations.

## 2. Proposed Repository Structure

```text
README.md
app.py
requirements.txt
Procfile
.gitignore

config.py                         # Small application constants

data_structures/
    __init__.py
    queue.py
    stack.py
    linked_list.py
    doubly_linked_list.py
    general_tree.py
    bst.py
    avl.py
    bplus_tree.py
    graph.py
    hash_table.py

visualization/
    __init__.py
    common.py                      # Shared Plotly styling and status colors
    linear.py                      # Queue, stack, linked-list figures
    tree.py                        # General tree, BST, AVL figures
    bplus_tree.py
    graph.py
    hash_table.py

ui/
    __init__.py
    layout.py                      # Dashboard layout and reusable controls
    callbacks.py                   # Dash callback wiring
    complexity.py                  # Display metadata, not algorithm logic

tests/
    test_queue.py
    test_stack.py
    test_linked_list.py
    test_doubly_linked_list.py
    test_general_tree.py
    test_bst.py
    test_avl.py
    test_bplus_tree.py
    test_graph.py
    test_hash_table.py

assets/
    style.css

docs/
    PHASE_1_PLAN.md
    VIVA_NOTES.md                 # Added alongside implementations
    REPORT.md                     # Written from verified implementation results

screenshots/                      # Only checked-in screenshots that actually exist
```

The structure keeps four responsibilities separate: algorithms in `data_structures`, Plotly figure construction in `visualization`, Dash state and controls in `ui`, and behavior verification in `tests`.

## 3. Data Model Decisions

### Common operation contract

Each public operation will either:

- return a useful value, such as a removed item, search result, or traversal list; or
- raise a small domain exception for invalid input or an operation that cannot be completed.

The Dash layer will catch expected domain exceptions and convert them into user-visible status messages. Unexpected programming errors should remain visible during development rather than being silently swallowed.

Every visualizer will receive a structure instance plus optional visual metadata:

```text
Structure state -> Plotly figure
Operation result -> status message + complexity record
```

Values will initially be integers. Input parsing and validation will be performed at the UI boundary, while structural invariants will also be protected inside the classes.

### Queue

Representation: Python list with a `front_index` is not required for the educational scale; a list with front at index 0 is simplest to explain. Enqueue appends, dequeue removes index 0. The visualizer shows Front and Rear explicitly.

Trade-off: dequeue is O(n) because the remaining list shifts. This is intentional and documented. A future optimized implementation could use `collections.deque`.

### Stack

Representation: Python list, with the end of the list as the top. Push and pop operate at the end, giving O(1) amortized time.

### Singly linked list

Representation: `Node(value, next)` plus a `head` reference and a length counter. Positions are zero-based. Supported insertions are beginning, end, and position; deletion will use a position or value consistently in the UI and tests (planned decision: delete by position to make duplicate handling deterministic).

### Doubly linked list

Representation: `Node(value, previous, next)` plus `head`, `tail`, and length. Traversal can proceed in either direction. Insertion/deletion by position will use the nearer end when locating a node where practical.

### General tree

Representation: a rooted node using a **first-child/next-sibling** model. This gives each node arbitrary children while also providing a binary projection for a defined inorder traversal:

- preorder: visit node, then each child subtree;
- postorder: visit each child subtree, then node;
- level order: breadth-first traversal;
- inorder: inorder traversal of the equivalent left-child/right-sibling representation, documented as a representation-specific traversal rather than a universal general-tree convention.

The UI will require a parent value when adding a non-root node. Deletion will remove a node and its subtree. Duplicate node values will be rejected to keep parent selection and visual labels unambiguous.

### Binary search tree

Representation: nodes with `value`, `left`, and `right`. Duplicate values will be rejected. Invariant: every value in the left subtree is less than the node and every value in the right subtree is greater. Deletion will handle leaf, one-child, and two-child cases using the inorder successor.

### AVL tree

Representation: BST nodes with a `height` field. Insert and delete will update heights while unwinding recursion and perform LL, RR, LR, or RL rotations based on balance factor. The class will expose balance factors and rotation information for the current operation so the visualizer can highlight the actual rotation performed.

Invariant for tests: `abs(height(left) - height(right)) <= 1` at every node after every mutation.

### B+ tree

Representation: configurable small order, default `order=4`, with internal nodes containing separator keys and child pointers, and leaf nodes containing sorted keys plus a `next_leaf` link. All records live in leaves; internal keys guide search.

Scope: educational integer-key B+ tree only, supporting insert, search, leaf traversal, splitting, and reset. Deletion is deliberately out of scope for the first implementation. A leaf split promotes a separator to the parent; internal splits propagate upward and may create a new root. Tests will verify sorted linked leaves and split behavior.

### Graph

Representation: undirected adjacency dictionary mapping a vertex to a set of neighbors. Vertices will use integer labels. Adding an existing edge will be idempotent; self-loops will be rejected initially. BFS and DFS will return traversal order and visited/traversed metadata for visualization. Deleting a vertex removes it from all neighbor sets.

### Hash table

Representation: fixed-capacity table using open addressing with linear probing. Each slot is either empty, occupied, or a tombstone after deletion. The default hash is `key % capacity`; capacity will be chosen as a small positive integer for readable diagrams. Duplicate inserts will update or reject consistently (planned decision: reject duplicates with a clear result).

The UI will show the initial hash index, collisions, probe sequence, and final slot when available. Average insert/search/delete is O(1) under a reasonable load factor; worst case is O(n).

## 4. Dashboard and State Design

The dashboard will have one main page with these regions:

1. Header: project title and concise academic description.
2. Data-structure selector: queue, stack, singly linked list, doubly linked list, general tree, BST, AVL, B+ tree, graph, or hash table.
3. Dynamic operation panel: only controls relevant to the selected structure.
4. Visualization panel: one Plotly `Graph` figure with stable dimensions.
5. Status panel: success/error message, operation result, and current traversal step.
6. Complexity panel: operation, time complexity, space complexity, and case notes.
7. History panel: a lightweight list of recent operations.

### State-management approach

Dash will use `dcc.Store` for serializable application state per browser session. The store will contain:

- selected structure name;
- serialized structure data or an operation replay sufficient to rebuild it;
- last operation and result metadata;
- history with a bounded number of entries;
- traversal steps and current step index when applicable.

The first implementation will favor serializing each structure's public state and reconstructing the class in the callback. This keeps classes independent of Dash and avoids storing live Python objects in browser state. A server-side session store is not required for this educational single-user-per-browser workflow.

Callbacks will be split by responsibility where practical: one callback for dynamic controls, one for operation submission/state transition, and one for rendering status, complexity, history, and figure. A reset action will create a fresh empty structure and clear operation-specific metadata.

## 5. Visualization Plan

A shared visual vocabulary will be used throughout:

- blue: ordinary node or bucket;
- green: inserted/currently selected item;
- amber: comparison or search target;
- red: deleted/error state;
- teal: visited/traversed item;
- orange: collision or rotation highlight.

These colors will be paired with text labels or symbols so meaning does not depend on color alone.

- Queue: horizontal boxes with Front and Rear labels and direction arrows.
- Stack: vertical boxes with a clear TOP label.
- Linked lists: node boxes with arrow segments; current node and changed node highlighted.
- General tree, BST, AVL: node-and-edge diagrams using deterministic hierarchical coordinates. AVL labels include balance factors; rotation metadata highlights affected nodes.
- B+ tree: internal and leaf node boxes, separator keys, and linked leaf-level arrows.
- Graph: vertices and edges using a deterministic layout; traversal metadata changes vertex and edge styling.
- Hash table: indexed row or grid with slot state, collision/probe information, and tombstones.

Traversal animation will begin as reliable step-by-step navigation: the operation creates an ordered list of steps, and Next/Previous controls select the displayed step. Auto-play can be considered only after this state model is stable.

## 6. Complexity Reference

The UI will distinguish typical, average, and worst-case claims where they differ. Space means auxiliary or structure storage as appropriate and will be explained in the documentation.

| Structure | Operation | Time | Notes |
|---|---|---:|---|
| Queue | enqueue | O(1) | list append |
| Queue | dequeue | O(n) | front removal shifts list |
| Queue | peek | O(1) | |
| Stack | push/pop/peek | O(1) amortized | list end |
| Singly list | insert beginning | O(1) | |
| Singly list | insert end/search/delete by position | O(n) | traversal required except head cases |
| Doubly list | insert/delete by position | O(n) | O(1) after node is located |
| General tree | add/search/traversal | O(n) | arbitrary tree traversal |
| BST | search/insert/delete | O(log n) average, O(n) worst | depends on height |
| AVL | search/insert/delete | O(log n) | balancing maintains logarithmic height |
| B+ tree | search/insert | O(log n) | educational in-memory tree |
| B+ tree | leaf traversal | O(n) | follows linked leaves |
| Graph | BFS/DFS | O(V + E) | adjacency sets |
| Hash table | insert/search/delete | O(1) average, O(n) worst | linear probing and load factor |

For each operation, the final UI complexity record will include the operation-specific claim rather than presenting one misleading complexity for the entire structure.

## 7. Development Roadmap

1. **Phase 1, current:** finalize architecture, representations, UI/state design, complexity reference, and testing strategy.
2. **Phase 2:** implement queue, stack, singly linked list, and doubly linked list with unit tests.
3. **Phase 3:** implement general tree, BST, and AVL; test invariants and all AVL rotations.
4. **Phase 4:** implement B+ tree, graph, and hash table; test splits, traversals, and collisions.
5. **Phase 5:** add focused Plotly visualizers for each structure.
6. **Phase 6:** assemble the unified Dash dashboard and dynamic controls.
7. **Phase 7:** add step navigation, bounded history, and readable random-data generation.
8. **Phase 8:** run the complete test suite, repair failures, and add edge-case coverage.
9. **Phase 9:** refine responsive styling, accessibility, error messages, and visual consistency.
10. **Phase 10:** write documentation and viva notes from the actual implementation.
11. **Phase 11:** prepare Git history, README, requirements, and deployment configuration.
12. **Phase 12:** deploy only after local verification; record the real URL and deployment result.
13. **Phase 13:** audit every assignment requirement with evidence and mark incomplete items honestly.

Each implementation phase will use small, meaningful commits rather than one generated project dump.

## 8. Testing Strategy

Use `pytest` for focused unit tests that do not require a running Dash server. Every structure gets normal-operation, empty-state, invalid-input, duplicate, missing-value, and reset tests where the behavior applies.

Critical assertions include:

- queue FIFO and stack LIFO behavior;
- linked-list pointer integrity in both directions;
- tree traversal order;
- BST ordering after insertions and all deletion cases;
- AVL balance factor and height invariant after each mutation, including LL, RR, LR, and RL examples;
- B+ tree sorted leaves, linked-leaf traversal, root/internal/leaf splits, and search after splits;
- graph BFS/DFS order, visited tracking, and vertex/edge deletion;
- hash-table collision resolution, tombstones, full-table behavior, and missing-key handling.

Visualization tests will initially check figure structure and labels rather than pixel-perfect output: expected traces, node labels, edge counts, and highlighted metadata. A small Dash smoke test will be added after the dashboard exists.

## 9. Error and Scope Policy

Expected user mistakes must become readable status messages, including empty operations, missing values, invalid positions, duplicate values, invalid graph edges, full hash tables, and malformed input. No callback should terminate the dashboard because of a normal user error.

The following are explicitly planned for later or excluded from the first stable version:

- B+ tree deletion;
- directed graph mode;
- production persistence or multi-user collaboration;
- AI-generated explanations;
- automatic traversal playback;
- bonus structures such as heaps or tries.

They must not be described as implemented until code and tests exist.

## 10. Phase 1 Acceptance Checklist

| Planning requirement | Status | Evidence |
|---|---|---|
| Architecture and folder structure | Complete | This document, sections 2 and 3 |
| Data model and representation choices | Complete | Section 3 |
| UI structure | Complete | Section 4 |
| State-management approach | Complete | Section 4 |
| Development roadmap | Complete | Section 7 |
| Complexity reference | Complete | Section 6 |
| Testing strategy | Complete | Section 8 |
| Core application implementation | Planned | Phase 2 onward |
| Automated tests | Planned | Phase 2 onward |
| Deployment | Planned | Phase 12, after verification |
| Screenshots and final report | Planned | After actual implementation |
