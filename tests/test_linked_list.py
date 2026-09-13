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


def test_singly_linked_list_deletes_head_middle_and_tail() -> None:
    linked_list = SinglyLinkedList([10, 20, 30, 40])

    assert linked_list.delete_at(0) == 10
    assert linked_list.delete_at(1) == 30
    assert linked_list.delete_at(1) == 40
    assert linked_list.traverse() == [20]
    assert linked_list.head is not None
    assert linked_list.head.next is None


def test_singly_linked_list_repeated_operations_keep_links_terminating() -> None:
    linked_list = SinglyLinkedList[int]()

    for value in range(10):
        linked_list.insert_end(value)
    for _ in range(5):
        linked_list.delete_at(0)
    linked_list.insert_beginning(99)
    linked_list.insert_at(3, 88)

    assert linked_list.traverse() == [99, 5, 6, 88, 7, 8, 9]
    assert linked_list.search(9) == 6
    assert linked_list.head is not None
    current = linked_list.head
    for _ in range(len(linked_list)):
        assert current is not None
        current = current.next
    assert current is None
