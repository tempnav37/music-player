from src.models import Track
from src.playlist_manager import PlaylistManager


def make_track(track_id: int) -> Track:
    return Track(track_id, f"Song {track_id}", "Artist", "Album", 180, "Pop")


def test_playlist_manager_add_play_next_previous_and_queue():
    manager = PlaylistManager([make_track(1), make_track(2), make_track(3)])

    assert manager.playlist.size == 3
    assert manager.current_track.id == 1

    manager.play_track(3)
    assert manager.current_track.id == 3

    next_track = manager.next_track()
    assert next_track.id == 1

    prev_track = manager.previous_track()
    assert prev_track.id == 3

    manager.add_to_queue(2)
    queued = manager.queue.peek()
    assert queued.id == 2

    next_queued = manager.next_track()
    assert next_queued.id == 2

    manager.clear_queue()
    assert len(manager.queue) == 0

    manager.clear_playlist()
    assert manager.playlist.size == 0
    assert manager.current_track is None


def test_playlist_manager_shuffle_and_modes():
    manager = PlaylistManager([make_track(1), make_track(2), make_track(3), make_track(4)])

    manager.shuffle_playlist()
    assert manager.playlist.size == 4
    assert set(track["id"] for track in manager.playlist.to_list()) == {1, 2, 3, 4}
    assert manager.playlist.validate() is True

    manager.set_mode("repeat_one")
    assert manager.playback_state.mode == "repeat_one"

    manager.set_mode("normal")
    assert manager.playback_state.mode == "normal"
