"""Модель музыкального артиста (группы, дуэта, сольного исполнителя)."""
from typing import Any, List, Optional

from .labels import Label, find_label_by_id


class Artist:
    """Музыкальный артист или группа."""

    def __init__(
        self,
        artist_id: int,
        name: str,
        country: str,
        label: Optional[Label] = None,
    ) -> None:
        self.id = artist_id
        self.name = name
        self.country = country
        self.label = label

    def __str__(self) -> str:
        label_name = self.label.name if self.label else "без лейбла"
        return f"{self.name} ({self.country}, {label_name})"

    @classmethod
    def from_data(
        cls,
        data: dict[str, Any],
        labels: List[Label],
    ) -> "Artist":
        """Создать артиста из словаря, подтянув связанный лейбл."""
        label = find_label_by_id(labels, data["label_id"])
        return cls(
            artist_id=data["id"],
            name=data["name"],
            country=data["country"],
            label=label,
        )

    def to_dict(self) -> dict[str, Any]:
        """Сериализация для JSON (храним id связанного лейбла)."""
        return {
            "id": self.id,
            "name": self.name,
            "country": self.country,
            "label_id": self.label.id if self.label else None,
        }


def find_artist_by_name(
    artists: List[Artist], name: str
) -> List[Artist]:
    """Ищет артистов по имени (регистронезависимо)."""
    query = name.lower()
    return [a for a in artists if query in a.name.lower()]


def get_artist_by_id(
    artists: List[Artist], artist_id: int
) -> Artist | None:
    """Находит артиста по ID."""
    for artist in artists:
        if artist.id == artist_id:
            return artist
    return None


def get_artists_by_label(
    artists: List[Artist], label: Label
) -> List[Artist]:
    """Возвращает список артистов лейбла."""
    return [
        a for a in artists
        if a.label is not None and a.label.id == label.id
    ]


def find_artists_for_request(
    artists: List[Artist], query: str, city: str = ""
) -> List[Artist]:
    """Подбирает артистов под заявку пользователя."""
    results: List[Artist] = []
    q = query.lower()
    city_lower = city.lower()
    for artist in artists:
        if q and q not in artist.name.lower():
            continue
        if city_lower and city_lower != artist.country.lower():
            continue
        results.append(artist)
    return results
