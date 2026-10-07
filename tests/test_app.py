from app import create_app


def test_app_home_and_api_endpoints():
    app = create_app()
    client = app.test_client()

    home_response = client.get('/')
    assert home_response.status_code == 200

    playlist_response = client.get('/api/playlist')
    assert playlist_response.status_code == 200
    payload = playlist_response.get_json()
    assert payload['success'] is True
    assert len(payload['playlist']) >= 1

    add_response = client.post('/api/playlist/add', json={
        'id': 99,
        'title': 'Demo Track',
        'artist': 'Demo Artist',
        'album': 'Demo Album',
        'duration': 180,
        'genre': 'Test',
    })
    assert add_response.status_code == 200

    play_response = client.post('/api/play/99')
    assert play_response.status_code == 200

    next_response = client.post('/api/next')
    assert next_response.status_code == 200

    previous_response = client.post('/api/previous')
    assert previous_response.status_code == 200

    shuffle_response = client.post('/api/shuffle')
    assert shuffle_response.status_code == 200

    queue_response = client.post('/api/queue/add', json={'track_id': 1})
    assert queue_response.status_code == 200

    queue_clear_response = client.post('/api/queue/clear')
    assert queue_clear_response.status_code == 200

    delete_response = client.delete('/api/playlist/99')
    assert delete_response.status_code == 200

    invalid_response = client.post('/api/mode', json={'mode': 'unknown'})
    assert invalid_response.status_code == 400
