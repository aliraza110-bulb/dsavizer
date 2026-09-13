"""Doubly linked list implementation for the visualizer."""

from collections.abc import Iterable
from typing import Generic, TypeVar


Value = TypeVar("Value")


class DoublyLinkedNode(Generic[Value]):
    """A node with pointers to both neighboring nodes."""

    def __init__(
        self,
        value: Value,
        previous: "DoublyLinkedNode[Value] | None" = None,
        next_node: "DoublyLinkedNode[Value] | None" = None,
    ) -> None:
        self.value = value
        self.previous = previous
        self.next = next_node


class DoublyLinkedList(Generic[Value]):
    """Doubly linked list with zero-based positional operations."""

    def __init__(self, values: Iterable[Value] | None = None) -> None:
        self.head: DoublyLinkedNode[Value] | None = None
        self.tail: DoublyLinkedNode[Value] | None = None
        self._length = 0
        for value in values or []:
            self.insert_end(value)

    def insert_at(self, position: int, value: Value) -> None:
        """Insert a value at a zero-based position."""
        self._validate_insert_position(position)
        node = DoublyLinkedNode(value)
        if self._length == 0:
            self.head = self.tail = node
        elif position == 0:
            assert self.head is not None
            node.next = self.head
            self.head.previous = node
            self.head = node
        elif position == self._length:
            assert self.tail is not None
            node.previous = self.tail
            self.tail.next = node
            self.tail = node
        else:
            next_node = self._node_at(position)
            previous = next_node.previous
            node.previous = previous
            node.next = next_node
            assert previous is not None
            previous.next = node
            next_node.previous = node
        self._length += 1

    def insert_beginning(self, value: Value) -> None:
        """Insert a value before the current head."""
        self.insert_at(0, value)

    def insert_end(self, value: Value) -> None:
        """Append a value after the current tail."""
        self.insert_at(self._length, value)

    def delete_at(self, position: int) -> Value:
        """Remove and return the value at a zero-based position."""
        self._validate_existing_position(position)
        node = self._node_at(position)
        if node.previous is None:
            self.head = node.next
        else:
            node.previous.next = node.next
        if node.next is None:
            self.tail = node.previous
        else:
            node.next.previous = node.previous
        self._length -= 1
        if self._length == 0:
            self.head = self.tail = None
        return node.value

    def search(self, value: Value) -> int:
        """Return the first matching position, or -1 when absent."""
        current = self.head
        position = 0
        while current is not None:
            if current.value == value:
                return position
            current = current.next
            position += 1
        return -1

    def traverse_forward(self) -> list[Value]:
        """Return values from head to tail."""
        values: list[Value] = []
        current = self.head
        while current is not None:
            values.append(current.value)
            current = current.next
        return values

    def traverse_backward(self) -> list[Value]:
        """Return values from tail to head."""
        values: list[Value] = []
        current = self.tail
        while current is not None:
            values.append(current.value)
            current = current.previous
        return values

    def clear(self) -> None:
        """Remove all nodes."""
        self.head = self.tail = None
        self._length = 0

    def __len__(self) -> int:
        return self._length

    def _node_at(self, position: int) -> DoublyLinkedNode[Value]:
        if position < self._length // 2:
            current = self.head
            for _ in range(position):
                assert current is not None
                current = current.next
        else:
            current = self.tail
            for _ in range(self._length - position - 1):
                assert current is not None
                current = current.previous
        assert current is not None
        return current

    def _validate_insert_position(self, position: int) -> None:
        if not 0 <= position <= self._length:
            raise IndexError(
                f"Position must be between 0 and {self._length} for insertion."
            )

    def _validate_existing_position(self, position: int) -> None:
        if not 0 <= position < self._length:
            raise IndexError(
                f"Position must be between 0 and {self._length - 1} for deletion."
            )
