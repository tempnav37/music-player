# Music Player Playlist & Queue Manager
## Academic Data Structures Project

A Flask-based web application demonstrating a **Circular Doubly Linked List** for music playlist management. This project combines practical data structures knowledge with an interactive frontend for playback simulation and visualization.

---

## Project Overview

This is a classroom mini-project for **Data Structures and Algorithms** demonstrating:

- **Core Data Structure**: A custom implementation of a Circular Doubly Linked List
- **Practical Application**: Music playlist management with queue support
- **Playback Simulation**: Visual and interactive music playback without external audio files
- **Educational Value**: Clear demonstration of linked-list operations and their complexity

The application is fully functional and educational, avoiding unnecessary external dependencies while maintaining clean, understandable code.

---

## Problem Statement

Music players typically cycle through playlists, moving forward and backward through songs. A **Circular Doubly Linked List** is an ideal data structure for this use case because:

1. **Circular navigation**: The last track naturally links back to the first.
2. **Bidirectional traversal**: Both forward and backward navigation are O(1).
3. **Efficient insertion/deletion**: Adding or removing tracks from any position.

This project demonstrates these advantages in a real-world context.

---

## Objectives

1. Implement a genuine **Circular Doubly Linked List** (not a Python list wrapper).
2. Use it as the core for playlist management.
3. Provide intuitive next/previous navigation using linked-list pointers.
4. Implement queue management for upcoming tracks.
5. Support shuffle while maintaining circular structure integrity.
6. Create a clean REST API for frontend interaction.
7. Build an interactive web UI with visualization.
8. Provide comprehensive unit tests.
9. Document complexity and academic concepts.

---

## Features

### Core Playlist Operations
- ✅ **Add Track**: Append a track to the playlist.
- ✅ **Remove Track**: Delete a track while maintaining circular structure.
- ✅ **Play Track**: Set a specific track as current.
- ✅ **Next Track**: Navigate to the next track using `current.next`.
- ✅ **Previous Track**: Navigate to the previous track using `current.prev`.
- ✅ **Clear Playlist**: Remove all tracks.

### Queue Management
- ✅ **Add to Queue**: Mark a track for immediate playback.
- ✅ **Remove from Queue**: Remove a track from the queue.
- ✅ **Clear Queue**: Empty the queue.
- ✅ **Queue Priority**: Queued tracks play before normal playlist navigation.

### Playback Features
- ✅ **Play/Pause**: Simulate continuous playback.
- ✅ **Progress Tracking**: Display elapsed and total time.
- ✅ **Progress Bar**: Visual representation of playback position.
- ✅ **Repeat Modes**:
  - Repeat All: Cycle through the entire playlist.
  - Repeat One: Repeat the current track indefinitely.
  - Normal: Play all tracks once.
- ✅ **Shuffle**: Randomize playlist order while preserving circular structure.

### Visualization
- ✅ **Linked List Display**: Show all nodes with connections.
- ✅ **Current Track Highlight**: Visual indication of the active track.
- ✅ **Neighbor Display**: Show previous, current, and next tracks.
- ✅ **Structure Validation**: Verify circular and doubly-linked properties.

---

## Technology Stack

### Backend
- **Python 3** — Programming language
- **Flask 3.0.3** — Web framework
- **JSON** — Data serialization

### Frontend
- **HTML5** — Markup
- **CSS3** — Styling
- **Vanilla JavaScript** — Interactivity (no frameworks)

### Testing
- **Pytest 8.3.2** — Unit testing framework

### Project Structure
```
Music Player/
├── app.py                          # Flask application entry point
├── requirements.txt                # Python dependencies
├── PROJECT_REQUIREMENTS.md         # Functional requirements
├── README.md                       # This file
│
├── src/
│   ├── __init__.py
│   ├── models.py                   # Track and PlaybackState dataclasses
│   ├── linked_list.py              # CircularDoublyLinkedList and Node classes
│   ├── queue_manager.py            # QueueManager class
│   └── playlist_manager.py         # PlaylistManager (orchestrator)
│
├── data/
│   └── sample_tracks.json          # 12 sample tracks
│
├── templates/
│   └── index.html                  # Frontend UI
│
├── static/
│   ├── css/
│   │   └── style.css               # Application styles
│   └── js/
│       └── app.js                  # Frontend logic and API integration
│
└── tests/
    ├── test_linked_list.py         # Circular Doubly Linked List tests
    ├── test_playlist_manager.py    # PlaylistManager tests
    └── test_app.py                 # Flask API endpoint tests
```

---

## Circular Doubly Linked List Explanation

### What is a Linked List?

A **linked list** is a data structure where each element (node) contains:
- Data (payload)
- A pointer to the next node

### What is a Doubly Linked List?

A **doubly linked list** extends the concept with:
- A pointer to the next node
- A pointer to the previous node

This enables **bidirectional traversal** without traversing from the head each time.

### What Makes it Circular?

A **circular linked list** connects the last node back to the first node:
- `last.next == first`
- `first.prev == last`

This creates a natural **continuous loop** for playlist playback—reaching the end automatically returns to the beginning.

### Why This Structure?

| Property | Array | Singly Linked List | Doubly Linked List | Circular Doubly |
|----------|-------|------------------|-------------------|-----------------|
| Random Access | O(1) | O(n) | O(n) | O(n) |
| Insert at head | O(n) | O(1) | O(1) | O(1) |
| Delete known node | O(n) | O(n) | O(1) | O(1) |
| Navigate next | O(1) | O(1) | O(1) | O(1) |
| Navigate previous | N/A | O(n) | O(1) | O(1) |
| Wrap-around (playlist loop) | Manual | Manual | Manual | Natural |

The **Circular Doubly Linked List** provides O(1) bidirectional navigation and natural loop behavior.

---

## Node Structure

```python
class Node:
    def __init__(self, track):
        self.track = track      # Track data (id, title, artist, etc.)
        self.prev = None        # Pointer to previous node
        self.next = None        # Pointer to next node
```

### Example: Three-Track Circular List

```
        ┌─────────────────────────────────┐
        ↓                                 │
    ┌─────────┐      ┌─────────┐      ┌─────────┐
    │ Track A │ ←──→ │ Track B │ ←──→ │ Track C │
    └─────────┘      └─────────┘      └─────────┘
        ↑                                 │
        └─────────────────────────────────┘

A.prev = C,  A.next = B
B.prev = A,  B.next = C
C.prev = B,  C.next = A
```

---

## Playlist Manager Architecture

### PlaylistManager
Acts as an orchestrator combining:
- Circular Doubly Linked List (core data structure)
- Queue Manager (upcoming tracks)
- Playback State (current mode, play/pause status)

### Key Operations

#### next()
```python
self.current = self.current.next  # O(1) - just follow the pointer
```

#### previous()
```python
self.current = self.current.prev  # O(1) - doubly linked advantage
```

#### shuffle()
```python
# Randomly rearrange node connections while maintaining circularity
for each node:
    randomly assign prev/next pointers
ensure: last.next = head and head.prev = last
```

---

## Queue Manager Architecture

The queue is a separate **FIFO (First-In-First-Out)** collection:
- Maintains tracks to be played **before** normal playlist navigation
- Supports add, remove, and clear operations
- Returns to normal playlist traversal once empty

### Queue Priority
```
Current: Track A
Queue: [Track D, Track F, Track B]

Playing sequence:
A → D → F → B → (resume playlist navigation)
```

---

## Complexity Analysis

| Operation | Complexity | Notes |
|-----------|-----------|-------|
| **Append** | O(1) | Tail insertion if tail reference maintained |
| **Prepend** | O(1) | Head insertion |
| **Insert After** | O(1) | If node is known |
| **Remove** | O(1) | If node is known |
| **Find by ID** | O(n) | Must traverse list |
| **Next** | O(1) | Follow `current.next` |
| **Previous** | O(1) | Follow `current.prev` |
| **Shuffle** | O(n) | Randomize order, maintain structure |
| **Traverse All** | O(n) | Visit each node once |

---

## Installation

### Requirements
- Python 3.8+
- pip (Python package manager)

### Setup

1. **Navigate to project directory**:
   ```bash
   cd "Music Player"
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## Running the Application

### Start the Flask Server
```bash
python app.py
```

Output:
```
 * Running on http://127.0.0.1:5000
```

### Access the Application
Open your web browser and navigate to:
```
http://127.0.0.1:5000
```

---

## Running Tests

### Execute All Tests
```bash
pytest
```

### Run Specific Test Files
```bash
pytest tests/test_linked_list.py      # Circular Doubly Linked List tests
pytest tests/test_playlist_manager.py # PlaylistManager tests
pytest tests/test_app.py              # Flask API tests
```

### View Test Coverage
```bash
pytest --cov=src
```

---

## API Endpoints

### Playlist Management

#### GET `/api/playlist`
Retrieve complete playlist state.

**Response**:
```json
{
  "success": true,
  "playlist": [
    {"id": 1, "title": "Song A", "artist": "Artist", ...},
    ...
  ],
  "current": {"id": 1, "title": "Song A", ...},
  "previous": {"id": 12, "title": "Song Z", ...},
  "next": {"id": 2, "title": "Song B", ...},
  "mode": "repeat_all",
  "visualization": {...}
}
```

#### POST `/api/playlist/add`
Add a new track to the playlist.

**Request**:
```json
{
  "id": 99,
  "title": "New Song",
  "artist": "New Artist",
  "album": "Album Name",
  "duration": 180,
  "genre": "Pop"
}
```

#### DELETE `/api/playlist/<track_id>`
Remove a track from the playlist.

#### POST `/api/play/<track_id>`
Set a specific track as current and play.

#### POST `/api/next`
Move to the next track.

#### POST `/api/previous`
Move to the previous track.

#### POST `/api/shuffle`
Randomize the playlist while maintaining structure.

#### POST `/api/playlist/clear`
Remove all tracks from the playlist.

### Queue Management

#### GET `/api/queue`
Retrieve the current queue.

#### POST `/api/queue/add`
Add a track to the queue.

**Request**:
```json
{"track_id": 5}
```

#### DELETE `/api/queue/<track_id>`
Remove a track from the queue.

#### POST `/api/queue/clear`
Clear the entire queue.

### Playback Control

#### POST `/api/mode`
Set playback mode.

**Request**:
```json
{"mode": "repeat_all"}
```

**Valid modes**: `"repeat_all"`, `"repeat_one"`, `"normal"`

---

## Frontend Usage

### Now Playing Section
- Displays current track metadata
- Shows progress bar and time remaining
- Play/Pause button to control simulation
- Previous/Next for navigation
- Shuffle to randomize
- Repeat to cycle through modes

### My Playlist
- Lists all tracks in order
- Current track is highlighted
- Buttons: Play, Queue, Delete

### Up Next (Queue)
- Shows queued tracks
- Remove individual tracks or clear all

### Visualization
- Displays all nodes with connections
- Shows HEAD pointer (first node)
- Highlights current node
- Displays neighbor relationships (prev/current/next)

---

## Edge Cases Handled

1. **Empty Playlist**
   - Gracefully shows "Playlist is empty"
   - All operations return appropriate errors

2. **Single-Node Playlist**
   - Correctly sets `node.next = node` and `node.prev = node`
   - Next/previous properly cycle

3. **Deletion**
   - Removes node while maintaining circular structure
   - Updates current pointer if deleted track was playing
   - Handles deletion of head, middle, and tail

4. **Shuffle**
   - Maintains exact track count
   - No duplicates or missing tracks
   - Structure remains circular

5. **Queue Priority**
   - Queued tracks play before playlist navigation
   - Empty queue returns to normal traversal

---

## Testing Coverage

### Linked List Tests (test_linked_list.py)
- Empty list handling
- Single-node playlist
- Multiple insertions
- Next/previous wraparound
- Node deletion (head, middle, last, only)
- Track finding
- Shuffle with structure validation
- Queue manager basic operations

### Playlist Manager Tests (test_playlist_manager.py)
- Add, remove, play, next, previous
- Queue operations
- Shuffle and mode switching
- Playlist clearing

### Flask API Tests (test_app.py)
- Home page load
- Playlist endpoint
- Add/delete track operations
- Playback control (play, next, previous)
- Shuffle functionality
- Queue operations
- Mode switching
- Error handling for invalid requests

---

## Viva Questions & Answers

### What is a linked list?
A linked list is a data structure where each element (node) contains data and a reference to the next node, forming a chain.

### What is a doubly linked list?
A doubly linked list extends the concept by having each node reference both the next and previous nodes, enabling bidirectional traversal.

### What makes this list circular?
The last node's `next` pointer points to the first node, and the first node's `prev` pointer points to the last node, creating a continuous loop.

### Why use a Circular Doubly Linked List for a music player?
- **Next/Previous are O(1)**: Direct pointer traversal.
- **Natural looping**: Reaching the end automatically returns to the start.
- **Bidirectional navigation**: Efficient backward movement.
- **Efficient insertion/deletion**: O(1) if node is known.

### How does Next work?
```python
self.current = self.current.next
```
It simply follows the `next` pointer to the adjacent node. At the end of the playlist, this naturally wraps to the first track.

### How does Previous work?
```python
self.current = self.current.prev
```
It follows the `prev` pointer. In a doubly linked list, this is direct and O(1), unlike a singly linked list which would require traversal.

### What happens when Next is pressed on the last song?
Because the last node's `next` points to the first node, navigation automatically wraps around to the beginning—demonstrating the circular property.

### Why is Previous efficient in a doubly linked list?
A doubly linked list stores both `prev` and `next` pointers, so backward navigation is direct (O(1)) without needing to traverse from the head.

### What happens when the list contains one node?
The node's `next` and `prev` both point to itself:
```python
node.next == node
node.prev == node
```
Next/previous operations work correctly, cycling through the single track.

### What is the complexity of searching for a track by ID?
O(n) — worst case requires traversing the entire list to find a specific track ID.

### What is the complexity of moving to the next track?
O(1) — a single pointer dereference (`current.next`).

### How does shuffle work?
The implementation randomly rearranges node connections while preserving:
- Exact track count (no duplicates or loss)
- Circular structure (`last.next = head`, `head.prev = last`)
- Doubly-linked property (every node's `prev.next == node`)

### What happens when a track is deleted?
The surrounding nodes are reconnected:
```python
node.prev.next = node.next
node.next.prev = node.prev
```
This maintains circular and doubly-linked properties for all remaining nodes.

### How do you maintain circularity after deletion?
After removing a node, if it was at the head, the head is updated. The new configuration automatically satisfies:
- `last.next == head`
- `head.prev == last`
- All intermediate nodes maintain their circular relationship

---

## Future Scope (Optional Enhancements)

1. **Actual Audio Playback**: Integrate with audio libraries for real music files.
2. **Persistent Storage**: Save playlists to a database.
3. **User Accounts**: Support multiple users with personalized playlists.
4. **Search**: Find tracks by title, artist, or genre.
5. **Sort**: Order playlist by various criteria.
6. **Favorite Tracks**: Mark and filter favorite tracks.
7. **Statistics**: Track playtime, most-played, etc.
8. **Keyboard Shortcuts**: Add keyboard controls.
9. **Drag-and-Drop Reordering**: Rearrange tracks via UI.
10. **Export Playlist**: Download playlist as JSON or CSV.

---

## Code Quality

- ✅ Meaningful variable and function names
- ✅ Type hints for clarity
- ✅ Docstrings where appropriate
- ✅ Clean separation of concerns
- ✅ Minimal code duplication
- ✅ No unnecessary external dependencies
- ✅ Follows PEP 8 conventions

---

## Known Limitations

1. No persistent storage—data resets on server restart.
2. No user authentication—single shared playlist.
3. No audio files—playback is simulated via frontend time tracking.
4. No external music APIs—works with hardcoded sample data.
5. Single-machine deployment—not optimized for concurrent users.

---

## Troubleshooting

### Issue: "ModuleNotFoundError" when running app
**Solution**: Ensure dependencies are installed:
```bash
pip install -r requirements.txt
```

### Issue: Port 5000 already in use
**Solution**: Use a different port:
```bash
python app.py --port 5001
```

### Issue: Tests fail with import errors
**Solution**: Ensure `src/` directory is in Python path. Run pytest from the project root:
```bash
cd "Music Player"
pytest
```

### Issue: Frontend shows "No queued tracks" even after adding queue
**Solution**: Refresh the browser or check browser console for JavaScript errors.

---

## References

- [Linked Lists - GeeksforGeeks](https://www.geeksforgeeks.org/linked-list-set-1-introduction/)
- [Circular Doubly Linked List - GeeksforGeeks](https://www.geeksforgeeks.org/circular-doubly-linked-list-introduction-and-insertion/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Data Structures](https://docs.python.org/3/tutorial/datastructures.html)

---

## Author

**Copilot** — AI Assistant  
Academic Data Structures Project  
2026

---

## License

Educational use only. Feel free to modify and distribute for learning purposes.

---

**Happy coding! 🎵**
