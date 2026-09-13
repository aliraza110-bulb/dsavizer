"""Educational general tree using a first-child/next-sibling representation."""

from collections import deque
from typing import Generic, TypeVar


Value = TypeVar("Value")


class GeneralTreeNode(Generic[Value]):
    def __init__(self, value: Value) -> None:
        self.value = value
        self.first_child: GeneralTreeNode[Value] | None = None
        self.next_sibling: GeneralTreeNode[Value] | None = None
        self.parent: GeneralTreeNode[Value] | None = None


class GeneralTree(Generic[Value]):
    """Rooted tree with arbitrary children and unique node values."""

    def __init__(self) -> None:
        self.root: GeneralTreeNode[Value] | None = None
        self._nodes: dict[Value, GeneralTreeNode[Value]] = {}

    def add_node(self, value: Value, parent_value: Value | None = None) -> None:
        if value in self._nodes:
            raise ValueError(f"Value {value!r} already exists in the tree.")
        if self.root is None:
            if parent_value is not None:
                raise ValueError("The first node must be the root.")
            self.root = GeneralTreeNode(value)
            self._nodes[value] = self.root
            return
        if parent_value is None or parent_value not in self._nodes:
            raise ValueError("A valid parent is required for a non-root node.")
        node = GeneralTreeNode(value)
        parent = self._nodes[parent_value]
        node.parent = parent
        if parent.first_child is None:
            parent.first_child = node
        else:
            sibling = parent.first_child
            while sibling.next_sibling is not None:
                sibling = sibling.next_sibling
            sibling.next_sibling = node
        self._nodes[value] = node

    def find(self, value: Value) -> GeneralTreeNode[Value] | None:
        return self._nodes.get(value)

    def delete(self, value: Value) -> None:
        node = self._nodes.get(value)
        if node is None:
            raise KeyError(f"Value {value!r} was not found.")
        if node.parent is None:
            self.root = None
        elif node.parent.first_child is node:
            node.parent.first_child = node.next_sibling
        else:
            previous = node.parent.first_child
            while previous is not None and previous.next_sibling is not node:
                previous = previous.next_sibling
            if previous is not None:
                previous.next_sibling = node.next_sibling
        self._remove_subtree(node)

    def preorder(self) -> list[Value]:
        result: list[Value] = []

        def visit(node: GeneralTreeNode[Value] | None) -> None:
            if node is None:
                return
            result.append(node.value)
            child = node.first_child
            while child is not None:
                visit(child)
                child = child.next_sibling

        visit(self.root)
        return result

    def postorder(self) -> list[Value]:
        result: list[Value] = []

        def visit(node: GeneralTreeNode[Value] | None) -> None:
            if node is None:
                return
            child = node.first_child
            while child is not None:
                visit(child)
                child = child.next_sibling
            result.append(node.value)

        visit(self.root)
        return result

    def inorder(self) -> list[Value]:
        """Traverse the binary left-child/right-sibling projection."""
        result: list[Value] = []

        def visit(node: GeneralTreeNode[Value] | None) -> None:
            if node is None:
                return
            visit(node.first_child)
            result.append(node.value)
            visit(node.next_sibling)

        visit(self.root)
        return result

    def level_order(self) -> list[Value]:
        if self.root is None:
            return []
        result: list[Value] = []
        pending: deque[GeneralTreeNode[Value]] = deque([self.root])
        while pending:
            node = pending.popleft()
            result.append(node.value)
            child = node.first_child
            while child is not None:
                pending.append(child)
                child = child.next_sibling
        return result

    def clear(self) -> None:
        self.root = None
        self._nodes.clear()

    def _remove_subtree(self, node: GeneralTreeNode[Value]) -> None:
        self._nodes.pop(node.value, None)
        child = node.first_child
        while child is not None:
            next_sibling = child.next_sibling
            self._remove_subtree(child)
            child = next_sibling
