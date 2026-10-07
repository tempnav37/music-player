from __future__ import annotations

from typing import Iterator

from .models import Track


class Node:
    def __init__(self, track: Track):
        self.track = track
        self.prev: Node | None = None
        self.next: Node | None = None

    def __repr__(self) -> str:
        return f"Node(id={self.track.id}, title={self.track.title!r})"

    def to_dict(self) -> dict:
        return {
            "id": self.track.id,
            "title": self.track.title,
            "artist": self.track.artist,
            "prev": self.prev.track.id if self.prev else None,
            "next": self.next.track.id if self.next else None,
        }


class CircularDoublyLinkedList:
    def __init__(self) -> None:
        self.head: Node | None = None
        self.current: Node | None = None
        self.size = 0

    def append(self, track: Track) -> Node:
        new_node = Node(track)
        if self.head is None:
            self.head = new_node
            self.current = new_node
            new_node.prev = new_node
            new_node.next = new_node
            self.size = 1
            return new_node

        tail = self.head.prev
        new_node.prev = tail
        new_node.next = self.head
        tail.next = new_node
        self.head.prev = new_node
        self.size += 1
        return new_node

    def prepend(self, track: Track) -> Node:
        new_node = Node(track)
        if self.head is None:
            return self.append(track)

        tail = self.head.prev
        new_node.prev = tail
        new_node.next = self.head
        self.head.prev = new_node
        tail.next = new_node
        self.head = new_node
        self.size += 1
        return new_node

    def insert_after(self, track_id: int, track: Track) -> Node:
        if self.head is None:
            return self.append(track)

        node = self.find(track_id)
        if node is None:
            raise ValueError(f"Track {track_id} not found.")

        new_node = Node(track)
        new_node.prev = node
        new_node.next = node.next
        node.next.prev = new_node
        node.next = new_node
        self.size += 1
        return new_node

    def remove(self, track_id: int) -> Track:
        if self.head is None:
            raise ValueError("Playlist is empty.")

        node = self.find(track_id)
        if node is None:
            raise ValueError(f"Track {track_id} not found.")

        if self.size == 1:
            removed_track = node.track
            self.head = None
            self.current = None
            self.size = 0
            return removed_track

        node.prev.next = node.next
        node.next.prev = node.prev

        if self.head == node:
            self.head = node.next
        if self.current == node:
            self.current = node.next

        self.size -= 1

        if self.size == 1:
            self.head.prev = self.head
            self.head.next = self.head
            self.current = self.head

        return node.track

    def find(self, track_id: int) -> Node | None:
        if self.head is None:
            return None

        node = self.head
        for _ in range(self.size):
            if node.track.id == track_id:
                return node
            node = node.next
        return None

    def next(self) -> Node:
        if self.current is None:
            raise ValueError("Playlist is empty.")
        self.current = self.current.next
        return self.current

    def previous(self) -> Node:
        if self.current is None:
            raise ValueError("Playlist is empty.")
        self.current = self.current.prev
        return self.current

    def get_current(self) -> Track | None:
        return self.current.track if self.current else None

    def set_current(self, track_id: int) -> Track:
        node = self.find(track_id)
        if node is None:
            raise ValueError(f"Track {track_id} not found.")
        self.current = node
        return node.track

    def to_list(self) -> list[dict]:
        if self.head is None:
            return []

        order: list[dict] = []
        node = self.head
        for _ in range(self.size):
            order.append(node.track.to_dict())
            node = node.next
        return order

    def get_length(self) -> int:
        return self.size

    def clear(self) -> None:
        self.head = None
        self.current = None
        self.size = 0

    def __iter__(self) -> Iterator[Node]:
        if self.head is None:
            return iter(())

        node = self.head
        for _ in range(self.size):
            yield node
            node = node.next

    def validate(self) -> bool:
        if self.head is None:
            return self.current is None and self.size == 0

        if self.size == 1:
            return self.head == self.current and self.head.next == self.head and self.head.prev == self.head

        node = self.head
        for _ in range(self.size):
            if node.next is None or node.prev is None:
                return False
            if node.next.prev != node or node.prev.next != node:
                return False
            node = node.next

        return node == self.head and self.head.prev.next == self.head and self.head.next.prev == self.head

    def visualization(self) -> dict:
        if self.head is None:
            return {"head": None, "current": None, "nodes": []}

        nodes = []
        node = self.head
        for _ in range(self.size):
            nodes.append({
                "id": node.track.id,
                "title": node.track.title,
                "artist": node.track.artist,
                "prev": node.prev.track.id if node.prev else None,
                "next": node.next.track.id if node.next else None,
            })
            node = node.next

        return {
            "head": self.head.track.id,
            "current": self.current.track.id if self.current else None,
            "nodes": nodes,
        }

    def shuffle(self) -> list[dict]:
        if self.size < 2:
            return self.to_list()

        current_id = self.current.track.id if self.current else None
        nodes = list(self)

        import random

        random.shuffle(nodes)
        for index, node in enumerate(nodes):
            node.prev = nodes[(index - 1) % len(nodes)]
            node.next = nodes[(index + 1) % len(nodes)]

        self.head = nodes[0]
        self.current = self.find(current_id) if current_id is not None else self.head

        if self.size == 1:
            self.head.prev = self.head
            self.head.next = self.head
            self.current = self.head

        return self.to_list()
