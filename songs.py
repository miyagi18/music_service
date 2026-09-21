from typing import List, Dict, Any


def find_song_by_title(
        songs: List[Dict[str, Any]], 
        title: str) -> List[Dict[str, Any]]:
    """Ищет песни по названию (регистронезависимо)."""
    results = []
    for song in songs:
        if title.lower() in song['title'].lower():
            results.append(song)
    return results


def get_songs_by_artist(
        songs: List[Dict[str, Any]], 
        artist_id: int) -> List[Dict[str, Any]]:
    """Возвращает список песен конкретного артиста."""
    results = []
    for song in songs:
        if song['artist_id'] == artist_id:
            results.append(song)
    return results