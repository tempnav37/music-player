const apiState = {
  playlist: [],
  queue: [],
  current: null,
  previous: null,
  next: null,
  mode: 'repeat_all',
  isPlaying: false,
  visualization: { nodes: [] },
};

let elapsedSeconds = 0;
let playbackTimer = null;

function formatTime(seconds) {
  if (seconds === null || Number.isNaN(seconds)) {
    return '00:00';
  }
  const total = Math.max(0, Math.floor(seconds));
  const mins = String(Math.floor(total / 60)).padStart(2, '0');
  const secs = String(total % 60).padStart(2, '0');
  return `${mins}:${secs}`;
}

async function apiRequest(url, method = 'GET', payload = null) {
  const headers = { 'Content-Type': 'application/json' };
  const options = {
    method,
    headers,
  };

  if (payload !== null) {
    options.body = JSON.stringify(payload);
  }

  const response = await fetch(url, options);
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.error || 'Request failed.');
  }
  return data;
}

function updateProgressBar() {
  const current = apiState.current;
  if (!current) {
    document.getElementById('progress-bar').style.width = '0%';
    return;
  }

  const duration = Number(current.duration || 0);
  const percentage = duration ? (elapsedSeconds / duration) * 100 : 0;
  document.getElementById('progress-bar').style.width = `${Math.min(percentage, 100)}%`;
}

function renderNowPlaying() {
  const current = apiState.current;
  const playButton = document.getElementById('play-btn');
  const repeatButton = document.getElementById('repeat-btn');

  if (!current) {
    document.getElementById('now-playing-title').textContent = 'Your playlist is empty.';
    document.getElementById('now-playing-artist').textContent = 'Add songs to get started.';
    document.getElementById('now-playing-album').textContent = 'No track selected';
    document.getElementById('current-time').textContent = '00:00';
    document.getElementById('total-time').textContent = '00:00';
    playButton.textContent = 'Play';
    repeatButton.textContent = 'Repeat: All';
    document.getElementById('progress-bar').style.width = '0%';
    return;
  }

  document.getElementById('now-playing-title').textContent = current.title;
  document.getElementById('now-playing-artist').textContent = current.artist;
  document.getElementById('now-playing-album').textContent = current.album;
  document.getElementById('current-time').textContent = formatTime(elapsedSeconds);
  document.getElementById('total-time').textContent = formatTime(current.duration);
  playButton.textContent = apiState.isPlaying ? 'Pause' : 'Play';
  repeatButton.textContent = `Repeat: ${apiState.mode === 'repeat_all' ? 'All' : apiState.mode === 'repeat_one' ? 'One' : 'Normal'}`;
  updateProgressBar();
}

function renderPlaylist() {
  const list = document.getElementById('playlist-list');
  const playlist = apiState.playlist;

  if (!playlist.length) {
    list.innerHTML = '<li class="empty-state">Your playlist is empty.<br/>Add some songs to get started.</li>';
    return;
  }

  list.innerHTML = playlist
    .map((track, index) => {
      const currentClass = apiState.current && track.id === apiState.current.id ? 'current' : '';
      return `
        <li class="track-row ${currentClass}">
          <div class="track-main">
            <span class="track-index">${index + 1}</span>
            <div class="track-info">
              <div class="track-title">${track.title}</div>
              <div class="track-artist">${track.artist}</div>
            </div>
          </div>
          <div class="track-actions">
            <button class="action-btn" data-action="play" data-track-id="${track.id}">Play</button>
            <button class="action-btn" data-action="queue" data-track-id="${track.id}">Queue</button>
            <button class="action-btn delete" data-action="delete" data-track-id="${track.id}">Delete</button>
          </div>
        </li>
      `;
    })
    .join('');

  list.querySelectorAll('[data-action]').forEach((button) => {
    button.addEventListener('click', async () => {
      const action = button.dataset.action;
      const trackId = Number(button.dataset.trackId);

      if (action === 'play') {
        await apiRequest(`/api/play/${trackId}`, 'POST');
        await refreshState();
        return;
      }

      if (action === 'queue') {
        await apiRequest('/api/queue/add', 'POST', { track_id: trackId });
        await refreshState();
        return;
      }

      if (action === 'delete') {
        await apiRequest(`/api/playlist/${trackId}`, 'DELETE');
        await refreshState();
      }
    });
  });
}

function renderQueue() {
  const list = document.getElementById('queue-list');
  const queue = apiState.queue;

  if (!queue.length) {
    list.innerHTML = '<li class="empty-state">No queued tracks.</li>';
    return;
  }

  list.innerHTML = queue
    .map((track, index) => `
      <li class="track-row">
        <div class="track-main">
          <span class="track-index">${index + 1}</span>
          <div class="track-info">
            <div class="track-title">${track.title}</div>
            <div class="track-artist">${track.artist}</div>
          </div>
        </div>
        <div class="track-actions">
          <button class="action-btn delete" data-action="queue-remove" data-track-id="${track.id}">Remove</button>
        </div>
      </li>
    `)
    .join('');

  list.querySelectorAll('[data-action="queue-remove"]').forEach((button) => {
    button.addEventListener('click', async () => {
      const trackId = Number(button.dataset.trackId);
      await apiRequest(`/api/queue/${trackId}`, 'DELETE');
      await refreshState();
    });
  });
}

function renderVisualization() {
  const container = document.getElementById('visualization');
  const nodes = apiState.visualization?.nodes || [];

  if (!nodes.length) {
    container.innerHTML = '<p class="empty-state">Your playlist is empty.</p>';
    document.getElementById('previous-label').textContent = '—';
    document.getElementById('current-label').textContent = '—';
    document.getElementById('next-label').textContent = '—';
    return;
  }

  const headId = apiState.visualization.head;
  const currentId = apiState.visualization.current;

  container.innerHTML = nodes
    .map((node) => {
      const classes = ['node-card'];
      if (node.id === currentId) classes.push('current');
      if (node.id === headId) classes.push('head');
      return `
        <div class="${classes.join(' ')}">
          <div class="node-card-header">
            <strong>${node.title}</strong>
            ${node.id === headId ? '<span class="tag">HEAD</span>' : ''}
          </div>
          <div class="node-links">Prev: ${node.prev ?? '—'} | Next: ${node.next ?? '—'}</div>
        </div>
      `;
    })
    .join('');

  const previousNode = apiState.previous || null;
  const currentNode = apiState.current || null;
  const nextNode = apiState.next || null;

  document.getElementById('previous-label').textContent = previousNode ? `${previousNode.title} (#${previousNode.id})` : '—';
  document.getElementById('current-label').textContent = currentNode ? `${currentNode.title} (#${currentNode.id})` : '—';
  document.getElementById('next-label').textContent = nextNode ? `${nextNode.title} (#${nextNode.id})` : '—';
}

async function refreshState() {
  try {
    const data = await apiRequest('/api/current');
    const state = data.state || data;

    apiState.playlist = state.playlist || [];
    apiState.queue = state.queue || [];
    apiState.current = state.current || null;
    apiState.previous = state.previous || null;
    apiState.next = state.next || null;
    apiState.mode = state.mode || 'repeat_all';
    apiState.isPlaying = Boolean(state.is_playing || false);
    apiState.visualization = state.visualization || { nodes: [], head: null, current: null };

    const currentTrack = apiState.current;
    elapsedSeconds = currentTrack ? Math.min(elapsedSeconds, currentTrack.duration || 0) : 0;

    renderNowPlaying();
    renderPlaylist();
    renderQueue();
    renderVisualization();
  } catch (error) {
    console.error(error);
  }
}

async function togglePlayback() {
  if (!apiState.current) {
    return;
  }

  apiState.isPlaying = !apiState.isPlaying;
  renderNowPlaying();
  if (apiState.isPlaying) {
    startPlaybackLoop();
  } else {
    stopPlaybackLoop();
  }
}

function startPlaybackLoop() {
  if (playbackTimer) {
    clearInterval(playbackTimer);
  }

  playbackTimer = setInterval(async () => {
    if (!apiState.isPlaying || !apiState.current) {
      return;
    }

    const duration = Number(apiState.current.duration || 0);
    elapsedSeconds += 1;

    if (elapsedSeconds >= duration) {
      elapsedSeconds = 0;
      try {
        await apiRequest('/api/next', 'POST');
        await refreshState();
      } catch (error) {
        console.error(error);
      }
      return;
    }

    updateProgressBar();
    document.getElementById('current-time').textContent = formatTime(elapsedSeconds);
  }, 1000);
}

function stopPlaybackLoop() {
  if (playbackTimer) {
    clearInterval(playbackTimer);
    playbackTimer = null;
  }
}

async function toggleRepeatMode() {
  const modes = ['repeat_all', 'repeat_one', 'normal'];
  const currentIndex = modes.indexOf(apiState.mode);
  const nextMode = modes[(currentIndex + 1) % modes.length];

  try {
    await apiRequest('/api/mode', 'POST', { mode: nextMode });
    await refreshState();
  } catch (error) {
    console.error(error);
  }
}

async function shufflePlaylist() {
  try {
    await apiRequest('/api/shuffle', 'POST');
    await refreshState();
  } catch (error) {
    console.error(error);
  }
}

async function clearPlaylist() {
  try {
    await apiRequest('/api/playlist/clear', 'POST');
    await refreshState();
  } catch (error) {
    console.error(error);
  }
}

async function clearQueue() {
  try {
    await apiRequest('/api/queue/clear', 'POST');
    await refreshState();
  } catch (error) {
    console.error(error);
  }
}

document.getElementById('play-btn').addEventListener('click', async () => {
  if (!apiState.current) {
    return;
  }
  if (apiState.isPlaying) {
    togglePlayback();
    return;
  }
  await refreshState();
  togglePlayback();
});

document.getElementById('previous-btn').addEventListener('click', async () => {
  try {
    await apiRequest('/api/previous', 'POST');
    elapsedSeconds = 0;
    await refreshState();
    if (apiState.current) {
      apiState.isPlaying = true;
      startPlaybackLoop();
    }
  } catch (error) {
    console.error(error);
  }
});

document.getElementById('next-btn').addEventListener('click', async () => {
  try {
    await apiRequest('/api/next', 'POST');
    elapsedSeconds = 0;
    await refreshState();
    if (apiState.current) {
      apiState.isPlaying = true;
      startPlaybackLoop();
    }
  } catch (error) {
    console.error(error);
  }
});

document.getElementById('shuffle-btn').addEventListener('click', async () => {
  await shufflePlaylist();
});

document.getElementById('repeat-btn').addEventListener('click', async () => {
  await toggleRepeatMode();
});

document.getElementById('clear-playlist-btn').addEventListener('click', async () => {
  await clearPlaylist();
});

document.getElementById('clear-queue-btn').addEventListener('click', async () => {
  await clearQueue();
});

window.addEventListener('DOMContentLoaded', async () => {
  await refreshState();
  renderNowPlaying();
});
