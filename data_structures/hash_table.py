"""Fixed-capacity hash table using linear probing."""

from typing import Generic, TypeVar


Key = TypeVar("Key", bound=int)
_TOMBSTONE = object()


class HashTable(Generic[Key]):
    """Hash table with open addressing and linear probing."""

    def __init__(self, capacity: int = 11) -> None:
        if capacity < 1:
            raise ValueError("Hash table capacity must be positive.")
        self.capacity = capacity
        self._slots: list[Key | object | None] = [None] * capacity

    def insert(self, key: Key) -> list[int]:
        """Insert a key and return the indexes checked during probing."""
        first_tombstone: int | None = None
        probes: list[int] = []
        for offset in range(self.capacity):
            index = (key + offset) % self.capacity
            probes.append(index)
            value = self._slots[index]
            if value == key:
                raise ValueError(f"Key {key!r} already exists.")
            if value is _TOMBSTONE and first_tombstone is None:
                first_tombstone = index
            elif value is None:
                self._slots[first_tombstone if first_tombstone is not None else index] = key
                return probes
        if first_tombstone is not None:
            self._slots[first_tombstone] = key
            return probes
        raise OverflowError("Hash table is full.")

    def search(self, key: Key) -> int:
        """Return the slot index for a key, or -1 when absent."""
        for offset in range(self.capacity):
            index = (key + offset) % self.capacity
            value = self._slots[index]
            if value is None:
                return -1
            if value is not _TOMBSTONE and value == key:
                return index
        return -1

    def delete(self, key: Key) -> None:
        index = self.search(key)
        if index == -1:
            raise KeyError(f"Key {key!r} was not found.")
        self._slots[index] = _TOMBSTONE

    def display(self) -> list[Key | str | None]:
        """Return user-facing slot contents for a table visualization."""
        return [
            "<deleted>" if value is _TOMBSTONE else value
            for value in self._slots
        ]

    def load_display(self, slots: list[Key | str | None]) -> None:
        """Restore the displayed slot state after a Dash callback round-trip."""
        if len(slots) != self.capacity:
            raise ValueError("Slot data does not match the table capacity.")
        self._slots = [
            _TOMBSTONE if value == "<deleted>" else value
            for value in slots
        ]

    def clear(self) -> None:
        self._slots = [None] * self.capacity
