from __future__ import annotations

from .linked_list import CircularDoublyLinkedList
from .models import PlaybackState, Track
from .queue_manager import QueueManager


class PlaylistManager:
    VALID_MODES = {"repeat_all", "repeat_one", "normal"}

    def __init__(self, tracks: list[Track] | None = None) -> None:
        self.playlist = CircularDoublyLinkedList()
        self.queue = QueueManager()
        self.playback_state = PlaybackState()

        if tracks:
            for track in tracks:
                self.add_track(track)

        if self.playlist.size > 0:
            self.playback_state.current_track_id = self.playlist.head.track.id
            self.playlist.current = self.playlist.head

    @property
    def current_track(self) -> Track | None:
        return self.playlist.get_current()

    @property
    def current_track_id(self) -> int | None:
        return self.playback_state.current_track_id

    def add_track(self, track: Track) -> Track:
        self.playlist.append(track)
        if self.playlist.size == 1:
            self.playback_state.current_track_id = track.id
            self.playlist.current = self.playlist.head
        return track

    def remove_track(self, track_id: int) -> Track:
        removed = self.playlist.remove(track_id)
        if self.playlist.size == 0:
            self.playback_state.current_track_id = None
            self.playback_state.progress_seconds = 0
            return removed

        if self.playback_state.current_track_id == track_id:
            self.playback_state.current_track_id = self.playlist.current.track.id if self.playlist.current else None
        return removed

    def get_track(self, track_id: int) -> Track | None:
        node = self.playlist.find(track_id)
        return node.track if node else None

    def play_track(self, track_id: int) -> Track:
        track = self.get_track(track_id)
        if track is None:
            raise ValueError(f"Track {track_id} not found.")
        self.playlist.set_current(track_id)
        self.playback_state.current_track_id = track_id
        self.playback_state.is_playing = True
        self.playback_state.progress_seconds = 0
        return track

    def next_track(self) -> Track:
        if self.playlist.size == 0:
            raise ValueError("Playlist is empty.")

        if self.queue:
            next_track = self.queue.pop_next()
            if next_track is None:
                raise ValueError("Queue is empty.")
            self.play_track(next_track.id)
            return self.current_track

        self.playlist.next()
        self.playback_state.current_track_id = self.playlist.current.track.id
        self.playback_state.is_playing = True
        self.playback_state.progress_seconds = 0
        return self.current_track

    def previous_track(self) -> Track:
        if self.playlist.size == 0:
            raise ValueError("Playlist is empty.")

        self.playlist.previous()
        self.playback_state.current_track_id = self.playlist.current.track.id
        self.playback_state.is_playing = True
        self.playback_state.progress_seconds = 0
        return self.current_track

    def shuffle_playlist(self) -> list[dict]:
        self.playlist.shuffle()
        if self.playlist.current is not None:
            self.playback_state.current_track_id = self.playlist.current.track.id
        return self.playlist.to_list()

    def add_to_queue(self, track_id: int) -> Track:
        track = self.get_track(track_id)
        if track is None:
            raise ValueError(f"Track {track_id} not found.")
        self.queue.add(track)
        return track

    def remove_from_queue(self, track_id: int) -> Track:
        return self.queue.remove(track_id)

    def clear_queue(self) -> None:
        self.queue.clear()

    def set_mode(self, mode: str) -> str:
        if mode not in self.VALID_MODES:
            raise ValueError(f"Unsupported mode: {mode}")
        self.playback_state.mode = mode
        return mode

    def clear_playlist(self) -> None:
        self.playlist.clear()
        self.queue.clear()
        self.playback_state.current_track_id = None
        self.playback_state.is_playing = False
        self.playback_state.progress_seconds = 0

    def current_neighbors(self) -> dict:
        if self.playlist.head is None or self.playlist.current is None:
            return {"previous": None, "current": None, "next": None}

        previous = self.playlist.current.prev.track if self.playlist.current.prev else None
        next_track = self.playlist.current.next.track if self.playlist.current.next else None
        return {
            "previous": previous.to_dict() if previous else None,
            "current": self.playlist.current.track.to_dict(),
            "next": next_track.to_dict() if next_track else None,
        }

    def api_state(self) -> dict:
        current = self.current_neighbors()
        state = {
            "success": True,
            "playlist": self.playlist.to_list(),
            "queue": self.queue.to_list(),
            "current": current["current"],
            "previous": current["previous"],
            "next": current["next"],
            "mode": self.playback_state.mode,
            "is_playing": self.playback_state.is_playing,
            "visualization": self.playlist.visualization(),
            "head": self.playlist.head.track.id if self.playlist.head else None,
            "current_id": self.playback_state.current_track_id,
        }
        return state
