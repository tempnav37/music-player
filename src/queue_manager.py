from __future__ import annotations

from collections import deque

from .models import Track


class QueueManager:
    def __init__(self) -> None:
        self._queue: deque[Track] = deque()

    def add(self, track: Track) -> None:
        if track not in self._queue:
            self._queue.append(track)

    def add_front(self, track: Track) -> None:
        if track not in self._queue:
            self._queue.appendleft(track)

    def remove(self, track_id: int) -> Track:
        for index, track in enumerate(self._queue):
            if track.id == track_id:
                del self._queue[index]
                return track
        raise ValueError(f"Track {track_id} not found in queue.")

    def clear(self) -> None:
        self._queue.clear()

    def pop_next(self) -> Track | None:
        if not self._queue:
            return None
        return self._queue.popleft()

    def peek(self) -> Track | None:
        if not self._queue:
            return None
        return self._queue[0]

    def to_list(self) -> list[dict]:
        return [track.to_dict() for track in self._queue]

    def __len__(self) -> int:
        return len(self._queue)

    def __bool__(self) -> bool:
        return bool(self._queue)
