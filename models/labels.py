"""Модель музыкального лейбла."""
from typing import Any, List


class Label:
    """Музыкальный лейбл."""

    def __init__(
        self,
        label_id: int,
        name: str,
        founded_year: int,
        country: str,
    ) -> None:
        self.id = label_id
        self.name = name
        self.founded_year = founded_year
        self.country = country

    def __str__(self) -> str:
        return f"{self.name} ({self.country}, {self.founded_year})"

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "Label":
        """Создать лейбл из словаря (данные из JSON)."""
        return cls(
            label_id=data["id"],
            name=data["name"],
            founded_year=data["founded_year"],
            country=data["country"],
        )

    def to_dict(self) -> dict[str, Any]:
        """Преобразовать объект в словарь для JSON."""
        return {
            "id": self.id,
            "name": self.name,
            "founded_year": self.founded_year,
            "country": self.country,
        }


def find_label_by_name(
    labels: List[Label], name: str
) -> List[Label]:
    """Ищет лейблы по названию (регистронезависимо)."""
    query = name.lower()
    return [label for label in labels if query in label.name.lower()]


def find_label_by_id(
    labels: List[Label], label_id: int
) -> Label | None:
    """Находит лейбл по ID."""
    for label in labels:
        if label.id == label_id:
            return label
    return None
