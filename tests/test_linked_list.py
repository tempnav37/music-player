from src.linked_list import CircularDoublyLinkedList
from src.models import Track


def make_track(track_id: int, title: str = "Song") -> Track:
    return Track(track_id, title, "Artist", "Album", 180, "Pop")


def assert_valid_cdll(cll: CircularDoublyLinkedList) -> None:
    if cll.size == 0:
        assert cll.head is None
        assert cll.current is None
        return

    node = cll.head
    visited = 0
    while visited < cll.size:
        assert node is not None
        assert node.next is not None
        assert node.prev is not None
        assert node.next.prev == node
        assert node.prev.next == node
        node = node.next
        visited += 1

    assert node == cll.head
    assert cll.head.prev.next == cll.head
    assert cll.head.next.prev == cll.head
    assert cll.validate() is True


def test_empty_list():
    cll = CircularDoublyLinkedList()
    assert cll.head is None
    assert cll.current is None
    assert cll.size == 0
    assert_valid_cdll(cll)


def test_single_node_list():
    cll = CircularDoublyLinkedList()
    track = make_track(1, "A")
    node = cll.append(track)

    assert cll.head == node
    assert cll.current == node
    assert cll.size == 1
    assert node.next == node
    assert node.prev == node
    assert_valid_cdll(cll)


def test_multiple_insertions():
    cll = CircularDoublyLinkedList()
    a = cll.append(make_track(1, "A"))
    b = cll.append(make_track(2, "B"))
    c = cll.append(make_track(3, "C"))

    assert a.next == b
    assert b.next == c
    assert c.next == a
    assert a.prev == c
    assert b.prev == a
    assert c.prev == b
    assert_valid_cdll(cll)


def test_next_wraparound():
    cll = CircularDoublyLinkedList()
    cll.append(make_track(1, "A"))
    cll.append(make_track(2, "B"))
    cll.append(make_track(3, "C"))

    cll.current = cll.head
    assert cll.next().track.title == "B"
    assert cll.next().track.title == "C"
    assert cll.next().track.title == "A"
    assert_valid_cdll(cll)


def test_previous_wraparound():
    cll = CircularDoublyLinkedList()
    cll.append(make_track(1, "A"))
    cll.append(make_track(2, "B"))
    cll.append(make_track(3, "C"))

    cll.current = cll.head
    assert cll.previous().track.title == "C"
    assert cll.previous().track.title == "B"
    assert cll.previous().track.title == "A"
    assert_valid_cdll(cll)


def test_delete_head():
    cll = CircularDoublyLinkedList()
    cll.append(make_track(1, "A"))
    cll.append(make_track(2, "B"))
    cll.append(make_track(3, "C"))

    removed = cll.remove(1)
    assert removed.id == 1
    assert cll.head.track.title == "B"
    assert cll.head.prev.track.title == "C"
    assert cll.head.next.track.title == "C"
    assert_valid_cdll(cll)


def test_delete_middle():
    cll = CircularDoublyLinkedList()
    cll.append(make_track(1, "A"))
    cll.append(make_track(2, "B"))
    cll.append(make_track(3, "C"))

    cll.remove(2)
    assert cll.head.track.title == "A"
    assert cll.head.next.track.title == "C"
    assert cll.head.prev.track.title == "C"
    assert_valid_cdll(cll)


def test_delete_last():
    cll = CircularDoublyLinkedList()
    cll.append(make_track(1, "A"))
    cll.append(make_track(2, "B"))
    cll.append(make_track(3, "C"))

    cll.remove(3)
    assert cll.head.track.title == "A"
    assert cll.head.next.track.title == "B"
    assert cll.head.prev.track.title == "B"
    assert_valid_cdll(cll)


def test_delete_only_node():
    cll = CircularDoublyLinkedList()
    cll.append(make_track(1, "A"))
    cll.remove(1)

    assert cll.head is None
    assert cll.current is None
    assert cll.size == 0
    assert_valid_cdll(cll)


def test_find_track():
    cll = CircularDoublyLinkedList()
    cll.append(make_track(1, "A"))
    cll.append(make_track(2, "B"))

    assert cll.find(1).track.title == "A"
    assert cll.find(99) is None
    assert_valid_cdll(cll)


def test_shuffle_preserves_structure():
    cll = CircularDoublyLinkedList()
    for value in (1, 2, 3, 4):
        cll.append(make_track(value, f"Song {value}"))

    original_ids = [node.track.id for node in cll]
    shuffled = cll.shuffle()
    shuffled_ids = [track["id"] for track in shuffled]

    assert len(shuffled_ids) == len(original_ids)
    assert set(shuffled_ids) == set(original_ids)
    assert len(shuffled_ids) == len(set(shuffled_ids))
    assert_valid_cdll(cll)


def test_queue_manager_basic_behavior():
    from src.queue_manager import QueueManager

    queue = QueueManager()
    track_a = make_track(1, "A")
    track_b = make_track(2, "B")

    queue.add(track_a)
    queue.add(track_b)
    assert queue.peek().id == 1
    assert queue.pop_next().id == 1
    assert queue.peek().id == 2
    queue.remove(2)
    assert len(queue) == 0
    queue.clear()
    assert len(queue) == 0
