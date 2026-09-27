"""Модель заявки пользователя на поиск музыкального коллектива."""
from typing import Any, List, Optional

from .artists import Artist, get_artist_by_id
from .users import User, find_user_by_id


STATUS_NEW = "new"
STATUS_IN_PROGRESS = "in_progress"
STATUS_DONE = "done"
STATUS_CANCELLED = "cancelled"

STATUS_LABELS = {
    STATUS_NEW: "Новая",
    STATUS_IN_PROGRESS: "В работе",
    STATUS_DONE: "Обработана",
    STATUS_CANCELLED: "Отменена",
}


class Request:
    """Заявка пользователя на поиск музыкального коллектива.

    Связывает объект User (кто оставил заявку) и, при обработке,
    объект Artist (какой коллектив был найден).
    """

    def __init__(
        self,
        request_id: int,
        user: User,
        query: str,
        genre: str = "",
        city: str = "",
        status: str = STATUS_NEW,
        created_at: str = "",
        found_artist: Optional[Artist] = None,
    ) -> None:
        self.id = request_id
        self.user = user
        self.query = query
        self.genre = genre
        self.city = city
        self.status = status
        self.created_at = created_at
        self.found_artist = found_artist

    def __str__(self) -> str:
        status = STATUS_LABELS.get(self.status, self.status)
        artist_name = self.found_artist.name if self.found_artist else "—"
        return (
            f"Заявка #{self.id} от {self.user.name}: «{self.query}» "
            f"[{status}], найденный коллектив: {artist_name}"
        )

    def is_active(self) -> bool:
        """Активна ли заявка."""
        return self.status in (STATUS_NEW, STATUS_IN_PROGRESS)

    def take_in_work(self) -> None:
        """Перевести заявку в работу."""
        self.status = STATUS_IN_PROGRESS

    def complete(self, artist: Artist) -> None:
        """Закрыть заявку, привязав найденный коллектив."""
        self.found_artist = artist
        self.status = STATUS_DONE

    def cancel(self) -> None:
        """Отменить заявку."""
        self.status = STATUS_CANCELLED

    @classmethod
    def from_data(
        cls,
        data: dict[str, Any],
        users: List[User],
        artists: List[Artist],
    ) -> Optional["Request"]:
        """Восстановить заявку из JSON, подтянув User и Artist."""
        user = find_user_by_id(users, data["user_id"])
        if user is None:
            return None
        artist: Optional[Artist] = None
        artist_id = data.get("artist_id")
        if artist_id is not None:
            artist = get_artist_by_id(artists, artist_id)
        return cls(
            request_id=data["id"],
            user=user,
            query=data["query"],
            genre=data.get("genre", ""),
            city=data.get("city", ""),
            status=data.get("status", STATUS_NEW),
            created_at=data.get("created_at", ""),
            found_artist=artist,
        )

    def to_dict(self) -> dict[str, Any]:
        """Сериализация: связанные объекты → их id."""
        return {
            "id": self.id,
            "user_id": self.user.id,
            "query": self.query,
            "genre": self.genre,
            "city": self.city,
            "status": self.status,
            "created_at": self.created_at,
            "artist_id": (
                self.found_artist.id if self.found_artist else None
            ),
        }


def create_request(
    requests: List[Request],
    request_id: int,
    user: User,
    query: str,
    genre: str = "",
    city: str = "",
    created_at: str = "",
) -> Request:
    """Создаёт заявку и добавляет её в коллекцию."""
    request = Request(
        request_id=request_id,
        user=user,
        query=query,
        genre=genre,
        city=city,
        created_at=created_at,
    )
    requests.append(request)
    return request


def get_user_requests(
    requests: List[Request], user: User
) -> List[Request]:
    """Все заявки конкретного пользователя."""
    return [r for r in requests if r.user.id == user.id]


def get_active_requests(requests: List[Request]) -> List[Request]:
    """Все активные заявки сервиса."""
    return [r for r in requests if r.is_active()]


def find_request_by_id(
    requests: List[Request], request_id: int
) -> Request | None:
    """Найти заявку по ID."""
    for request in requests:
        if request.id == request_id:
            return request
    return None


def next_request_id(requests: List[Request]) -> int:
    """Следующий свободный id заявки."""
    if not requests:
        return 1
    return max(r.id for r in requests) + 1
