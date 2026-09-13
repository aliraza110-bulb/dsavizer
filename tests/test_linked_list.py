import pytest

from data_structures.linked_list import SinglyLinkedList


def test_singly_linked_list_insert_search_and_delete() -> None:
    linked_list = SinglyLinkedList[int]()
    linked_list.insert_beginning(20)
    linked_list.insert_end(40)
    linked_list.insert_at(1, 30)

    assert linked_list.traverse() == [20, 30, 40]
    assert linked_list.search(30) == 1
    assert linked_list.search(99) == -1
    assert linked_list.delete_at(1) == 30
    assert linked_list.traverse() == [20, 40]


def test_singly_linked_list_allows_duplicates_and_resets() -> None:
    linked_list = SinglyLinkedList([ ])
    linked_list.insert_end(5)
    linked_list.insert_end(5)

    assert linked_list.search(5) == 0
    linked_list.clear()
    assert linked_list.traverse() == []
    assert len(linked_list) == 0


def test_singly_linked_list_rejects_invalid_positions() -> None:
    linked_list = SinglyLinkedList[int]()

    with pytest.raises(IndexError):
        linked_list.delete_at(0)
    with pytest.raises(IndexError):
        linked_list.insert_at(1, 10)
