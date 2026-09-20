from typing import List, Dict, Any

def get_artist_by_id(artists: list[dict[str, Any]], artist_id: int) -> list[dict[str, Any]] | None:
    for artist in artist:
        if artist["id"] == artist_id:
            return artist
    return None


def find_artist_by_name(artists: List[Dict[str, Any]], name: str) -> List[Dict[str, Any]]:
    """Ищет артистов по имени."""
    results = []
    for artist in artists:
        if name.lower() in artist['name'].lower():
            results.append(artist)
    return results

def get_artists_by_label(artists: List[Dict[str, Any]], label_id: int) -> List[Dict[str, Any]]:
    """Возвращает список артистов, принадлежащих лейблу."""
    results = []
    for artist in artists:
        if artist['label_id'] == label_id:
            results.append(artist)
    return results