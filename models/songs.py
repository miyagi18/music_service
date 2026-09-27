"""Модель песни."""
from typing import Any, List, Optional

from .artists import Artist, get_artist_by_id


class Song:
    """Музыкальная композиция."""

    def __init__(
        self,
        song_id: int,
        title: str,
        artist: Artist,
        genre: str,
        release_year: int,
        duration_sec: int,
        has_lyrics: bool = False,
    ) -> None:
        self.id = song_id
        self.title = title
        self.artist = artist
        self.genre = genre
        self.release_year = release_year
        self.duration_sec = duration_sec
        self.has_lyrics = has_lyrics

    def __str__(self) -> str:
        lyrics = (
            "текст доступен" if self.has_lyrics
            else "текст не доступен"
        )
        return (
            f"{self.title} ({self.release_year}) — "
            f"{self.artist.name}, {self.genre}. {lyrics}"
        )

    @classmethod
    def from_data(
        cls,
        data: dict[str, Any],
        artists: List[Artist],
    ) -> Optional["Song"]:
        """Создать песню, связав её с артистом.

        Возвращает None, если артист не найден.
        """
        artist = get_artist_by_id(artists, data["artist_id"])
        if artist is None:
            return None
        return cls(
            song_id=data["id"],
            title=data["title"],
            artist=artist,
            genre=data["genre"],
            release_year=data["release_year"],
            duration_sec=data["duration_sec"],
            has_lyrics=data.get("has_lyrics", False),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "artist_id": self.artist.id,
            "genre": self.genre,
            "release_year": self.release_year,
            "duration_sec": self.duration_sec,
            "has_lyrics": self.has_lyrics,
        }


def find_song_by_title(
    songs: List[Song], title: str
) -> List[Song]:
    """Ищет песни по названию (регистронезависимо)."""
    query = title.lower()
    return [s for s in songs if query in s.title.lower()]


def get_songs_by_artist(
    songs: List[Song], artist: Artist
) -> List[Song]:
    """Возвращает песни конкретного артиста."""
    return [s for s in songs if s.artist.id == artist.id]


def get_songs_by_label(
    songs: List[Song], artists: List[Artist], label_id: int
) -> List[Song]:
    """Возвращает песни всех артистов лейбла."""
    label_artist_ids = {
        a.id for a in artists
        if a.label is not None and a.label.id == label_id
    }
    return [s for s in songs if s.artist.id in label_artist_ids]
