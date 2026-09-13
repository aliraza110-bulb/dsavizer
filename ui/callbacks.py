"""Dash callbacks and serialization boundary for the visualizer."""

from __future__ import annotations

import random
from typing import Any

from dash import ALL, Input, Output, State, html, ctx

from data_structures import (
    AVLTree,
    BinarySearchTree,
    BPlusTree,
    DoublyLinkedList,
    GeneralTree,
    Graph,
    HashTable,
    Queue,
    SinglyLinkedList,
    Stack,
)
from data_structures.avl import AVLNode
from data_structures.bst import BSTNode
from visualization.bplus_tree import bplus_tree_figure
from visualization.graph import graph_figure
from visualization.hash_table import hash_table_figure
from visualization.linear import linked_list_figure, linear_figure
from visualization.tree import binary_tree_figure, general_tree_figure

from .complexity import COMPLEXITIES
from .layout import OPERATIONS


def empty_state(structure: str) -> dict[str, Any]:
    state: dict[str, Any] = {
        "structure": structure,
        "values": [],
        "history": [],
        "steps": [],
        "step_index": 0,
    }
    if structure == "General Tree":
        state["nodes"] = []
    elif structure in {"Binary Search Tree", "AVL Tree"}:
        state["tree"] = None
    elif structure == "Graph":
        state["vertices"] = []
        state["edges"] = []
    elif structure == "Hash Table":
        state["capacity"] = 11
    return state


def build_structure(state: dict[str, Any]) -> Any:
    structure = state["structure"]
    values = state.get("values", [])
    if structure == "Queue":
        return Queue(values)
    if structure == "Stack":
        return Stack(values)
    if structure == "Singly Linked List":
        return SinglyLinkedList(values)
    if structure == "Doubly Linked List":
        return DoublyLinkedList(values)
    if structure == "General Tree":
        tree = GeneralTree()
        for node in state.get("nodes", []):
            tree.add_node(node["value"], node["parent"])
        return tree
    if structure == "Binary Search Tree":
        tree = BinarySearchTree(values)
        if state.get("tree") is not None:
            tree.root = restore_tree_node(state["tree"], False)
        return tree
    if structure == "AVL Tree":
        tree = AVLTree(values)
        if state.get("tree") is not None:
            tree.root = restore_tree_node(state["tree"], True)
        return tree
    if structure == "B+ Tree":
        tree = BPlusTree()
        if state.get("bplus_tree") is not None:
            tree.root = restore_bplus_node(state["bplus_tree"])
        else:
            for value in values:
                tree.insert(value)
        return tree
    if structure == "Graph":
        graph = Graph()
        for vertex in state.get("vertices", []):
            graph.add_vertex(vertex)
        for first, second in state.get("edges", []):
            graph.add_edge(first, second)
        return graph
    if structure == "Hash Table":
        table = HashTable(state.get("capacity", 11))
        if state.get("slots") is not None:
            table.load_display(state["slots"])
        else:
            for value in values:
                table.insert(value)
        return table
    raise ValueError(f"Unknown structure: {structure}")


def sync_state(state: dict[str, Any], structure: Any) -> dict[str, Any]:
    name = state["structure"]
    state["values"] = []
    if name in {"Queue", "Stack", "Singly Linked List", "Doubly Linked List"}:
        state["values"] = structure.to_list() if name in {"Queue", "Stack"} else structure.traverse_forward() if name == "Doubly Linked List" else structure.traverse()
    elif name == "General Tree":
        state["nodes"] = [
            {"value": value, "parent": structure.find(value).parent.value if structure.find(value).parent else None}
            for value in structure.preorder()
        ]
    elif name in {"Binary Search Tree", "AVL Tree"}:
        state["values"] = structure.inorder()
        state["tree"] = snapshot_tree_node(structure.root)
    elif name == "B+ Tree":
        state["values"] = structure.leaf_traversal()
        state["bplus_tree"] = snapshot_bplus_node(structure.root)
    elif name == "Graph":
        state["vertices"] = list(structure.adjacency)
        state["edges"] = [
            [first, second]
            for first in structure.adjacency
            for second in structure.adjacency[first]
            if str(first) < str(second)
        ]
    elif name == "Hash Table":
        state["slots"] = structure.display()
        state["values"] = [value for value in state["slots"] if isinstance(value, int)]
    return state


def snapshot_tree_node(node: Any) -> dict[str, Any] | None:
    if node is None:
        return None
    return {
        "value": node.value,
        "left": snapshot_tree_node(node.left),
        "right": snapshot_tree_node(node.right),
        "height": getattr(node, "height", None),
    }


def restore_tree_node(data: dict[str, Any] | None, avl: bool) -> Any:
    if data is None:
        return None
    node = (AVLNode if avl else BSTNode)(data["value"])
    node.left = restore_tree_node(data.get("left"), avl)
    node.right = restore_tree_node(data.get("right"), avl)
    if avl:
        node.height = data.get("height") or 1
    return node


def snapshot_bplus_node(node: Any) -> dict[str, Any]:
    return {
        "is_leaf": node.is_leaf,
        "keys": list(node.keys),
        "children": [snapshot_bplus_node(child) for child in node.children],
    }


def restore_bplus_node(data: dict[str, Any]) -> Any:
    from data_structures.bplus_tree import BPlusNode

    node = BPlusNode(is_leaf=data["is_leaf"], keys=list(data["keys"]))
    node.children = [restore_bplus_node(child) for child in data.get("children", [])]
    leaves: list[Any] = []

    def collect(current: Any) -> None:
        if current.is_leaf:
            leaves.append(current)
            return
        for child in current.children:
            collect(child)

    collect(node)
    for first, second in zip(leaves, leaves[1:]):
        first.next_leaf = second
    return node


def figure_for(state: dict[str, Any], structure: Any, mode: str = "3D"):
    name = state["structure"]
    steps = state.get("steps", [])
    index = state.get("step_index", 0)
    highlight = steps[index] if steps and index < len(steps) else None
    if name == "Queue":
        return linear_figure(structure.to_list(), "queue", highlight, mode)
    if name == "Stack":
        return linear_figure(structure.to_list(), "stack", highlight, mode)
    if name == "Singly Linked List":
        return linked_list_figure(structure.traverse(), False, highlight, mode)
    if name == "Doubly Linked List":
        return linked_list_figure(structure.traverse_forward(), True, highlight, mode)
    if name == "General Tree":
        return general_tree_figure(structure.root, mode, highlight)
    if name == "Binary Search Tree":
        return binary_tree_figure(structure.root, "Binary Search Tree", mode=mode, highlight=highlight)
    if name == "AVL Tree":
        return binary_tree_figure(structure.root, "AVL Tree (balance factors)", True, mode, highlight)
    if name == "B+ Tree":
        return bplus_tree_figure(structure.root, mode, highlight)
    if name == "Graph":
        return graph_figure(structure.adjacency, set(steps[: index + 1]), mode)
    if name == "Hash Table":
        return hash_table_figure(structure.display(), mode, highlight)
    raise ValueError(f"Unknown structure: {name}")


def as_number(value: Any) -> int:
    if value is None or value == "":
        raise ValueError("A numeric value is required.")
    return int(value)


def as_graph_value(value: Any) -> Any:
    if value is None or str(value).strip() == "":
        raise ValueError("A vertex value is required.")
    text = str(value).strip()
    try:
        return int(text)
    except ValueError:
        return text


def random_state(structure: str) -> dict[str, Any]:
    state = empty_state(structure)
    values = random.sample(range(10, 90), 6)
    if structure == "General Tree":
        state["nodes"] = [{"value": 1, "parent": None}]
        state["nodes"] += [{"value": value, "parent": 1} for value in values[:3]]
        state["nodes"] += [{"value": values[3], "parent": values[0]}]
    elif structure == "Graph":
        state["vertices"] = list(range(1, 6))
        state["edges"] = [[1, 2], [1, 3], [2, 4], [3, 5]]
    elif structure == "Hash Table":
        state["values"] = [11, 22, 33, 47]
    else:
        state["values"] = values
    return state


def search_path(root: Any, target: int) -> list[int]:
    path: list[int] = []
    node = root
    while node is not None:
        value = int(getattr(node, "value"))
        path.append(value)
        if value == target:
            break
        node = getattr(node, "left" if target < value else "right", None)
    return path


def explanation_for(structure: str, operation: str, message: str) -> str:
    explanations = {
        "Queue": "A queue uses FIFO order: enqueue adds at the rear and dequeue removes from the front.",
        "Stack": "A stack uses LIFO order: push adds to the top and pop removes the most recent item.",
        "Singly Linked List": "Follow each next pointer in order; insertion and deletion update the affected link.",
        "Doubly Linked List": "Each node keeps previous and next links, so updates preserve both directions.",
        "General Tree": "Tree operations move through parent-child relationships from the root.",
        "Binary Search Tree": "Compare at each node: smaller values move left and larger values move right.",
        "AVL Tree": "The AVL tree maintains balance factors and rotates when a subtree becomes unbalanced.",
        "B+ Tree": "Internal keys guide the search while linked leaves keep the sorted values together.",
        "Graph": "Traversal records the order in which vertices are visited while exploring connections.",
        "Hash Table": "The hash index is checked first; collisions continue through the next available slot.",
    }
    return f"Operation: {operation}. {explanations.get(structure, '')} {message}"


def friendly_error(error: Exception) -> str:
    text = str(error)
    if isinstance(error, (TypeError, ValueError)) and "required" in text.lower():
        return "Please enter a value before running this operation."
    if isinstance(error, (IndexError, KeyError)):
        return text.replace("'", "")
    if isinstance(error, OverflowError):
        return "The structure is full. Reset it or remove an item first."
    return text or "The operation could not be completed."


def register_callbacks(app: Any) -> None:
    @app.callback(
        Output("operation-buttons", "children"),
        Input("structure-selector", "value"),
    )
    def update_operations(structure: str):
        operations = OPERATIONS[structure]
        return html.Div(
            [
                html.Button(
                    operation,
                    id={"type": "operation-button", "operation": operation},
                    n_clicks=0,
                    className="primary-button" if operation in {"Insert", "Push", "Enqueue", "Insert Beginning", "Insert End", "Add Node", "Add Vertex", "Add Edge"} else "secondary-button",
                )
                for operation in operations
            ],
            className="operation-list",
        )

    @app.callback(
        Output("value-input", "style"),
        Output("secondary-input", "style"),
        Output("value-label", "children"),
        Output("secondary-label", "children"),
        Input("structure-selector", "value"),
        Input({"type": "operation-button", "operation": ALL}, "n_clicks"),
    )
    def update_input_visibility(structure: str, _operation_clicks: list[int] | None):
        triggered = ctx.triggered_id
        operation = triggered.get("operation") if isinstance(triggered, dict) else OPERATIONS[structure][0]
        no_value = operation in {"Dequeue", "Pop", "Peek", "Display", "Traverse", "Forward Traversal", "Backward Traversal", "Minimum", "Maximum", "Inorder", "Preorder", "Postorder", "Level Order", "Height", "Leaf Traversal"}
        if operation == "Delete" and structure in {"Singly Linked List", "Doubly Linked List"}:
            no_value = True
        needs_secondary = structure in {"Singly Linked List", "Doubly Linked List", "General Tree", "Graph"}
        value_label = "Key" if structure == "Hash Table" else "Vertex" if structure == "Graph" else "Child" if structure == "General Tree" and operation == "Add Child" else "Value"
        secondary_label = "Parent" if structure == "General Tree" and operation == "Add Child" else "To" if structure == "Graph" and operation in {"Add Edge", "Delete Edge"} else "Position / second value"
        return ({"display": "none"} if no_value else {}), ({"display": "block"} if needs_secondary else {"display": "none"}), value_label, secondary_label

    @app.callback(
        Output("animation-timer", "disabled"),
        Input("animation-play", "n_clicks"),
        Input("animation-pause", "n_clicks"),
        Input("animation-timer", "n_intervals"),
        Input("state-store", "data"),
    )
    def update_animation_timer(_play: int, _pause: int, _timer: int, state: dict[str, Any] | None):
        if ctx.triggered_id == "animation-pause":
            return True
        if ctx.triggered_id == "animation-play":
            return not bool(state and state.get("steps"))
        if ctx.triggered_id == "animation-timer":
            steps = state.get("steps", []) if state else []
            return not steps or state.get("step_index", 0) >= len(steps) - 1
        return True

    @app.callback(
        Output("animation-timer", "interval"),
        Input("animation-speed", "value"),
    )
    def update_animation_speed(speed: int):
        return speed or 900

    @app.callback(
        Output("state-store", "data"),
        Output("structure-graph", "figure"),
        Output("status-panel", "children"),
        Output("complexity-panel", "children"),
        Output("history-panel", "children"),
        Output("step-label", "children"),
        Output("explanation-panel", "children"),
        Output("animation-controls", "style"),
        Input("structure-selector", "value"),
        Input({"type": "operation-button", "operation": ALL}, "n_clicks"),
        Input("reset-button", "n_clicks"),
        Input("random-button", "n_clicks"),
        Input("previous-button", "n_clicks"),
        Input("next-button", "n_clicks"),
        Input("animation-previous", "n_clicks"),
        Input("animation-next", "n_clicks"),
        Input("animation-timer", "n_intervals"),
        Input("view-mode", "value"),
        State("value-input", "value"),
        State("secondary-input", "value"),
        State("state-store", "data"),
    )
    def update_dashboard(structure: str, _operation_clicks: list[int] | None, _reset: int, _random: int, _previous: int, _next: int, _animation_previous: int, _animation_next: int, _timer: int, view_mode: str, value: Any, secondary: Any, stored: dict[str, Any] | None):
        trigger = ctx.triggered_id
        operation = trigger.get("operation") if isinstance(trigger, dict) else OPERATIONS[structure][0]
        state = empty_state(structure) if trigger == "structure-selector" or not stored or stored.get("structure") != structure else stored
        message = "Ready. Choose an operation."
        if trigger == "reset-button":
            state = empty_state(structure)
            message = f"{structure} reset."
        elif trigger == "random-button":
            state = random_state(structure)
            message = f"Generated readable sample data for {structure}."
        elif isinstance(trigger, str) and trigger in {"previous-button", "next-button", "animation-previous", "animation-next", "animation-timer"} and state.get("steps"):
            step_count = len(state["steps"])
            delta = -1 if trigger in {"previous-button", "animation-previous"} else 1
            state["step_index"] = max(0, min(step_count - 1, state.get("step_index", 0) + delta))
            message = f"Traversal step {state['step_index'] + 1} of {step_count}."
            if trigger == "animation-timer" and state["step_index"] >= step_count - 1:
                state["animation_playing"] = False
        elif isinstance(trigger, dict) and trigger.get("type") == "operation-button":
            structure_object = build_structure(state)
            try:
                result = perform_operation(state, structure_object, operation, value, secondary)
                state = sync_state(state, structure_object)
                state["steps"] = result.get("steps", [])
                state["step_index"] = 0
                message = result["message"]
                state["history"] = ([message] + state.get("history", []))[:8]
            except (IndexError, KeyError, ValueError, OverflowError, TypeError) as error:
                message = friendly_error(error)
                state["history"] = ([message] + state.get("history", []))[:8]
        structure_object = build_structure(state)
        complexity = COMPLEXITIES.get(structure, {}).get(operation, ("-", "-"))
        complexity_panel = [html.P(f"Operation: {operation}"), html.P(f"Time: {complexity[0]}"), html.P(f"Space: {complexity[1]}")]
        history_panel = [html.Li(item) for item in state.get("history", [])]
        steps = state.get("steps", [])
        step_label = f"Step {state.get('step_index', 0) + 1} of {len(steps)}: {steps[state.get('step_index', 0)]}" if steps else "No traversal active"
        return state, figure_for(state, structure_object, view_mode), message, complexity_panel, history_panel, step_label, explanation_for(structure, operation, message), {} if steps else {"display": "none"}


def perform_operation(state: dict[str, Any], structure: Any, operation: str, value: Any, secondary: Any) -> dict[str, Any]:
    name = state["structure"]
    if name == "Queue":
        if operation == "Enqueue":
            number = as_number(value); structure.enqueue(number); return {"message": f"Enqueued {number}.", "steps": [number]}
        if operation == "Dequeue":
            removed = structure.dequeue(); return {"message": f"Dequeued {removed}.", "steps": [removed]}
        if operation == "Peek":
            front = structure.peek(); return {"message": f"Front is {front}.", "steps": [front]}
        return {"message": f"Queue contains {len(structure)} item(s)."}
    if name == "Stack":
        if operation == "Push":
            number = as_number(value); structure.push(number); return {"message": f"Pushed {number}.", "steps": [number]}
        if operation == "Pop":
            removed = structure.pop(); return {"message": f"Popped {removed}.", "steps": [removed]}
        if operation == "Peek":
            top = structure.peek(); return {"message": f"Top is {top}.", "steps": [top]}
        return {"message": f"Stack contains {len(structure)} item(s)."}
    if name in {"Singly Linked List", "Doubly Linked List"}:
        position = as_number(secondary) if operation in {"Insert Position", "Delete"} else None
        if operation == "Insert Beginning":
            structure.insert_beginning(as_number(value)); return {"message": f"Inserted {value} at the beginning."}
        if operation == "Insert End":
            structure.insert_end(as_number(value)); return {"message": f"Inserted {value} at the end."}
        if operation == "Insert Position":
            structure.insert_at(position, as_number(value)); return {"message": f"Inserted {value} at position {position}."}
        if operation == "Delete":
            return {"message": f"Deleted {structure.delete_at(position)} from position {position}."}
        if operation == "Search":
            target = as_number(value); found = structure.search(target); values = structure.traverse_forward() if name == "Doubly Linked List" else structure.traverse(); return {"message": f"Value found at position {found}." if found >= 0 else "Value not found.", "steps": values[:found + 1] if found >= 0 else values}
        values = structure.traverse_forward() if name == "Doubly Linked List" else structure.traverse()
        if operation == "Forward Traversal":
            values = structure.traverse_forward()
        if operation == "Backward Traversal":
            values = structure.traverse_backward()
        return {"message": "Traversal: " + " -> ".join(map(str, values)), "steps": values}
    if name == "General Tree":
        if operation == "Create Root":
            structure.add_node(as_number(value)); return {"message": f"Created root {value}."}
        if operation == "Add Child":
            structure.add_node(as_number(value), as_number(secondary)); return {"message": f"Added child {value} to parent {secondary}."}
        if operation == "Delete Node":
            structure.delete(as_number(value)); return {"message": f"Deleted node {value} and its subtree."}
        if operation == "Search":
            target = as_number(value)
            found = structure.find(target) is not None
            return {"message": f"Node {target} found." if found else f"Node {target} was not found.", "steps": [target]}
        values = getattr(structure, operation.lower().replace(" ", "_"))()
        return {"message": operation + ": " + " -> ".join(map(str, values)), "steps": values}
    if name in {"Binary Search Tree", "AVL Tree"}:
        if operation == "Insert":
            rotation = structure.insert(as_number(value)); return {"message": f"Inserted {value}." + (f" Rotation: {rotation}." if rotation else "")}
        if operation == "Search":
            target = as_number(value); found = structure.search(target); return {"message": "Value found." if found else "Value not found.", "steps": search_path(structure.root, target)}
        if operation == "Delete":
            rotation = structure.delete(as_number(value)); return {"message": f"Deleted {value}." + (f" Rotation: {rotation}." if rotation else "")}
        if operation == "Minimum":
            return {"message": f"Minimum is {structure.minimum()}."}
        if operation == "Maximum":
            return {"message": f"Maximum is {structure.maximum()}."}
        if operation == "Height":
            return {"message": f"Height is {structure.height()}."}
        values = getattr(structure, operation.lower().replace(" ", "_"))()
        return {"message": operation + ": " + " -> ".join(map(str, values)), "steps": values}
    if name == "B+ Tree":
        if operation == "Insert":
            split = structure.insert(as_number(value)); return {"message": f"Inserted key {value}." + (" A node split occurred." if split else "")}
        if operation == "Search":
            target = as_number(value)
            return {"message": "Key found." if structure.search(target) else "Key not found.", "steps": [target]}
        values = structure.leaf_traversal()
        return {"message": "Leaf traversal: " + " -> ".join(map(str, values)), "steps": values}
    if name == "Graph":
        first = as_graph_value(value)
        second = as_graph_value(secondary) if secondary is not None and str(secondary).strip() else None
        if operation == "Add Vertex":
            structure.add_vertex(first); return {"message": f"Added vertex {first}."}
        if operation == "Add Edge":
            if second is None:
                raise ValueError("Enter both endpoints for an edge.")
            structure.add_edge(first, second); return {"message": f"Added edge {first} - {second}."}
        if operation == "Delete Vertex":
            structure.delete_vertex(first); return {"message": f"Deleted vertex {first}."}
        if operation == "Delete Edge":
            if second is None:
                raise ValueError("Enter both endpoints for an edge.")
            structure.delete_edge(first, second); return {"message": f"Deleted edge {first} - {second}."}
        values = structure.bfs(first) if operation == "BFS" else structure.dfs(first)
        return {"message": operation + ": " + " -> ".join(map(str, values)), "steps": values}
    if name == "Hash Table":
        if operation == "Insert":
            probes = structure.insert(as_number(value)); return {"message": f"Inserted {value}; probes checked: {probes}.", "steps": probes}
        if operation == "Search":
            target = as_number(value); index = structure.search(target); return {"message": f"Found at index {index}." if index >= 0 else "Value not found.", "steps": [index] if index >= 0 else []}
        if operation == "Delete":
            structure.delete(as_number(value)); return {"message": f"Deleted {value}."}
        return {"message": "Displayed hash table contents."}
    raise ValueError(f"Unsupported operation: {operation}")
