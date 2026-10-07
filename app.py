from __future__ import annotations

import json
from pathlib import Path

from flask import Flask, jsonify, render_template, request

from src.models import Track
from src.playlist_manager import PlaylistManager

BASE_DIR = Path(__file__).resolve().parent
DATA_FILE = BASE_DIR / "data" / "sample_tracks.json"


def load_default_tracks() -> list[Track]:
    with DATA_FILE.open("r", encoding="utf-8") as handle:
        raw_tracks = json.load(handle)
    return [Track.from_dict(track) for track in raw_tracks]


def create_app() -> Flask:
    app = Flask(__name__, template_folder="templates", static_folder="static")
    manager = PlaylistManager(load_default_tracks())

    @app.route("/")
    def index() -> str:
        return render_template("index.html")

    @app.route("/api/playlist")
    def api_playlist():
        return jsonify(manager.api_state())

    @app.route("/api/current")
    def api_current():
        return jsonify(manager.api_state())

    @app.route("/api/playlist/add", methods=["POST"])
    def add_track():
        payload = request.get_json(silent=True) or {}
        try:
            track = Track(
                id=payload.get("id"),
                title=payload.get("title"),
                artist=payload.get("artist"),
                album=payload.get("album"),
                duration=payload.get("duration"),
                genre=payload.get("genre"),
            )
            if not all([track.id, track.title, track.artist, track.album, track.duration is not None, track.genre]):
                raise ValueError("Missing required track fields.")
            manager.add_track(track)
            return jsonify({"success": True, "track": track.to_dict(), "state": manager.api_state()})
        except Exception as exc:  # pragma: no cover - defensive route handling
            return jsonify({"success": False, "error": str(exc)}), 400

    @app.route("/api/playlist/<int:track_id>", methods=["DELETE"])
    def delete_track(track_id: int):
        try:
            track = manager.remove_track(track_id)
            return jsonify({"success": True, "removed": track.to_dict(), "state": manager.api_state()})
        except ValueError as exc:
            return jsonify({"success": False, "error": str(exc)}), 404

    @app.route("/api/play/<int:track_id>", methods=["POST"])
    def play_track(track_id: int):
        try:
            track = manager.play_track(track_id)
            return jsonify({"success": True, "current": track.to_dict(), "state": manager.api_state()})
        except ValueError as exc:
            return jsonify({"success": False, "error": str(exc)}), 404

    @app.route("/api/next", methods=["POST"])
    def next_track():
        try:
            track = manager.next_track()
            return jsonify({"success": True, "current": track.to_dict(), "state": manager.api_state()})
        except ValueError as exc:
            return jsonify({"success": False, "error": str(exc)}), 404

    @app.route("/api/previous", methods=["POST"])
    def previous_track():
        try:
            track = manager.previous_track()
            return jsonify({"success": True, "current": track.to_dict(), "state": manager.api_state()})
        except ValueError as exc:
            return jsonify({"success": False, "error": str(exc)}), 404

    @app.route("/api/shuffle", methods=["POST"])
    def shuffle_tracks():
        try:
            playlist = manager.shuffle_playlist()
            return jsonify({"success": True, "playlist": playlist, "state": manager.api_state()})
        except Exception as exc:  # pragma: no cover - defensive route handling
            return jsonify({"success": False, "error": str(exc)}), 400

    @app.route("/api/playlist/clear", methods=["POST"])
    def clear_playlist():
        manager.clear_playlist()
        return jsonify({"success": True, "state": manager.api_state()})

    @app.route("/api/queue")
    def queue_state():
        return jsonify({"success": True, "queue": manager.queue.to_list(), "state": manager.api_state()})

    @app.route("/api/queue/add", methods=["POST"])
    def add_queue():
        payload = request.get_json(silent=True) or {}
        track_id = payload.get("track_id")
        if track_id is None:
            return jsonify({"success": False, "error": "track_id is required."}), 400
        try:
            track = manager.add_to_queue(track_id)
            return jsonify({"success": True, "track": track.to_dict(), "queue": manager.queue.to_list(), "state": manager.api_state()})
        except ValueError as exc:
            return jsonify({"success": False, "error": str(exc)}), 404

    @app.route("/api/queue/<int:track_id>", methods=["DELETE"])
    def delete_queue(track_id: int):
        try:
            track = manager.remove_from_queue(track_id)
            return jsonify({"success": True, "removed": track.to_dict(), "queue": manager.queue.to_list(), "state": manager.api_state()})
        except ValueError as exc:
            return jsonify({"success": False, "error": str(exc)}), 404

    @app.route("/api/queue/clear", methods=["POST"])
    def clear_queue():
        manager.clear_queue()
        return jsonify({"success": True, "queue": manager.queue.to_list(), "state": manager.api_state()})

    @app.route("/api/mode", methods=["POST"])
    def set_mode():
        payload = request.get_json(silent=True) or {}
        mode = payload.get("mode")
        if not mode:
            return jsonify({"success": False, "error": "mode is required."}), 400
        try:
            manager.set_mode(mode)
            return jsonify({"success": True, "mode": manager.playback_state.mode, "state": manager.api_state()})
        except ValueError as exc:
            return jsonify({"success": False, "error": str(exc)}), 400

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
