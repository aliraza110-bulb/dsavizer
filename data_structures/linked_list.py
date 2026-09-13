"""Singly linked list implementation for the visualizer."""

from collections.abc import Iterable
from typing import Generic, TypeVar


Value = TypeVar("Value")


class LinkedNode(Generic[Value]):
    """A node containing a value and a pointer to the next node."""

    def __init__(self, value: Value, next_node: "LinkedNode[Value] | None" = None) -> None:
        self.value = value
        self.next = next_node


class SinglyLinkedList(Generic[Value]):
    """Singly linked list with zero-based positional operations."""

    def __init__(self, values: Iterable[Value] | None = None) -> None:
        self.head: LinkedNode[Value] | None = None
        self._length = 0
        for value in values or []:
            self.insert_end(value)

    def insert_beginning(self, value: Value) -> None:
        """Insert a value before the current head."""
        self.head = LinkedNode(value, self.head)
        self._length += 1

    def insert_end(self, value: Value) -> None:
        """Append a value after the current tail."""
        self.insert_at(self._length, value)

    def insert_at(self, position: int, value: Value) -> None:
        """Insert a value at a zero-based position."""
        self._validate_insert_position(position)
        if position == 0:
            self.insert_beginning(value)
            return

        previous = self._node_at(position - 1)
        previous.next = LinkedNode(value, previous.next)
        self._length += 1

    def delete_at(self, position: int) -> Value:
        """Remove and return the value at a zero-based position."""
        self._validate_existing_position(position)
        if position == 0:
            assert self.head is not None
            removed = self.head
            self.head = removed.next
        else:
            previous = self._node_at(position - 1)
            assert previous.next is not None
            removed = previous.next
            previous.next = removed.next
        self._length -= 1
        return removed.value

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

    def traverse(self) -> list[Value]:
        """Return values from head to tail."""
        values: list[Value] = []
        current = self.head
        while current is not None:
            values.append(current.value)
            current = current.next
        return values

    def clear(self) -> None:
        """Remove all nodes."""
        self.head = None
        self._length = 0

    def __len__(self) -> int:
        return self._length

    def _node_at(self, position: int) -> LinkedNode[Value]:
        current = self.head
        for _ in range(position):
            assert current is not None
            current = current.next
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
