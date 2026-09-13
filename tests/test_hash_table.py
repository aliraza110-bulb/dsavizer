import pytest

from data_structures.hash_table import HashTable


def test_hash_table_resolves_collisions_with_linear_probing() -> None:
    table = HashTable[int](capacity=5)
    probes = table.insert(1)
    probes_for_collision = table.insert(6)

    assert probes == [1]
    assert probes_for_collision == [1, 2]
    assert table.search(1) == 1
    assert table.search(6) == 2


def test_hash_table_tombstones_preserve_probe_chain() -> None:
    table = HashTable[int](capacity=5)
    table.insert(1)
    table.insert(6)
    table.delete(1)

    assert table.search(6) == 2
    assert table.display()[1] == "<deleted>"
    assert table.search(99) == -1


def test_hash_table_rejects_duplicates_and_full_table() -> None:
    table = HashTable[int](capacity=2)
    table.insert(1)
    table.insert(2)

    with pytest.raises(ValueError):
        table.insert(1)
    with pytest.raises(OverflowError):
        table.insert(3)
    with pytest.raises(KeyError):
        table.delete(99)
