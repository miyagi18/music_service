"""Модель пользователя сервиса."""
from typing import Any, List


class User:
    """Пользователь сервиса поиска музыкальных коллективов."""

    def __init__(
        self,
        user_id: int,
        name: str,
        email: str,
        city: str = "",
    ) -> None:
        self.id = user_id
        self.name = name
        self.email = email
        self.city = city

    def __str__(self) -> str:
        return f"{self.name} <{self.email}> ({self.city})"

    @classmethod
    def from_data(cls, data: dict[str, Any]) -> "User":
        """Создать пользователя из словаря."""
        return cls(
            user_id=data["id"],
            name=data["name"],
            email=data["email"],
            city=data.get("city", ""),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "city": self.city,
        }


def find_user_by_name(
    users: List[User], name: str
) -> List[User]:
    """Ищет пользователей по имени."""
    query = name.lower()
    return [u for u in users if query in u.name.lower()]


def find_user_by_id(
    users: List[User], user_id: int
) -> User | None:
    """Находит пользователя по ID."""
    for user in users:
        if user.id == user_id:
            return user
    return None
