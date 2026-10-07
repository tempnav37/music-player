from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class Track:
    id: int
    title: str
    artist: str
    album: str
    duration: int
    genre: str

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, value: dict) -> "Track":
        return cls(
            id=value["id"],
            title=value["title"],
            artist=value["artist"],
            album=value["album"],
            duration=value["duration"],
            genre=value["genre"],
        )


@dataclass
class PlaybackState:
    is_playing: bool = False
    mode: str = "repeat_all"
    current_track_id: int | None = None
    progress_seconds: int = 0
