from songs import find_song_by_title, get_songs_by_artist


mock_songs = [
    {"id": 1, "title": "Bismarck", "artist_id": 2, "release_year": 2018},
    {"id": 2, "title": "Колизей", "artist_id": 1, "release_year": 2017}
]


def test_find_song_by_title():
    """Тест поиска песни по названию."""
    result = find_song_by_title(mock_songs, "bismarck")
    assert len(result) == 1
    assert result[0]['title'] == "Bismarck"


def test_find_song_not_found():
    """Тест поиска несуществующей песни."""
    result = find_song_by_title(mock_songs, "Unknown")
    assert len(result) == 0


def test_get_songs_by_artist():
    """Тест получения песен артиста по ID."""
    result = get_songs_by_artist(mock_songs, 2)
    assert len(result) == 1
    assert result[0]['artist_id'] == 2
    