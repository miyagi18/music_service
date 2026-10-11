"""Тесты модели Request — заявки пользователя на поиск коллектива."""

from models import Artist, Request, User
from models.requests import (
    STATUS_CANCELLED,
    STATUS_DONE,
    STATUS_IN_PROGRESS,
    STATUS_NEW,
    create_request,
    find_request_by_id,
    get_active_requests,
    get_user_requests,
    next_request_id,
)


# ---------- создание объекта ----------

def test_request_creation_defaults() -> None:
    """При создании заявка имеет статус new и не активна."""
    user = User(1, "Иван", "ivan@example.com")
    request = Request(1, user, "Miyagi")
    assert request.id == 1
    assert request.user is user
    assert request.query == "Miyagi"
    assert request.status == STATUS_NEW
    assert request.found_artist is None
    assert request.is_active()


def test_request_str() -> None:
    """Строка заявки содержит статус и пользователя."""
    user = User(1, "Иван", "ivan@example.com")
    request = Request(1, user, "Miyagi")
    text = str(request)
    assert "Заявка #1" in text
    assert "Иван" in text
    assert "Miyagi" in text
    assert "Новая" in text


# ---------- жизненный цикл статусов (бизнес-логика) ----------

def test_request_take_in_work() -> None:
    """Перевод заявки в работу."""
    user = User(1, "Иван", "ivan@example.com")
    request = Request(1, user, "Miyagi")
    request.take_in_work()
    assert request.status == STATUS_IN_PROGRESS
    assert request.is_active()


def test_request_complete() -> None:
    """Закрытие заявки с привязкой найденного артиста."""
    user = User(1, "Иван", "ivan@example.com")
    artist = Artist(1, "Miyagi", "Россия")
    request = Request(1, user, "Miyagi")
    request.complete(artist)
    assert request.status == STATUS_DONE
    assert request.found_artist is artist
    assert not request.is_active()


def test_request_cancel() -> None:
    """Отмена заявки."""
    user = User(1, "Иван", "ivan@example.com")
    request = Request(1, user, "Miyagi")
    request.cancel()
    assert request.status == STATUS_CANCELLED
    assert not request.is_active()


def test_request_str_shows_completed_artist() -> None:
    """После закрытия строка заявки содержит имя найденного артиста."""
    user = User(1, "Иван", "ivan@example.com")
    artist = Artist(1, "Miyagi", "Россия")
    request = Request(1, user, "Miyagi")
    request.complete(artist)
    text = str(request)
    assert "Miyagi" in text
    assert "Обработана" in text


# ---------- from_data / to_dict ----------

def test_request_from_data_links_user_and_artist() -> None:
    """from_data восстанавливает объекты User и Artist по id."""
    users = [User(1, "Иван", "ivan@example.com")]
    artists = [Artist(1, "Miyagi", "Россия")]
    data = {
        "id": 10,
        "user_id": 1,
        "query": "Miyagi",
        "genre": "Hip-Hop",
        "city": "Москва",
        "status": "done",
        "created_at": "2026-09-15",
        "artist_id": 1,
    }
    request = Request.from_data(data, users, artists)
    assert request is not None
    assert request.user.id == 1
    assert request.found_artist is not None
    assert request.found_artist.id == 1
    assert request.status == "done"


def test_request_from_data_user_not_found() -> None:
    """Если user_id не найден — возвращается None."""
    data = {
        "id": 10,
        "user_id": 99,
        "query": "Miyagi",
        "status": "new",
    }
    assert Request.from_data(data, [], []) is None


def test_request_from_data_without_artist() -> None:
    """Если artist_id = None — found_artist остаётся None."""
    users = [User(1, "Иван", "ivan@example.com")]
    data = {
        "id": 10,
        "user_id": 1,
        "query": "Miyagi",
        "status": "new",
        "artist_id": None,
    }
    request = Request.from_data(data, users, [])
    assert request is not None
    assert request.found_artist is None


def test_request_to_dict_stores_ids() -> None:
    """to_dict хранит user_id и artist_id, а не объекты."""
    user = User(1, "Иван", "ivan@example.com")
    artist = Artist(5, "Miyagi", "Россия")
    request = Request(10, user, "Miyagi")
    request.complete(artist)
    data = request.to_dict()
    assert data["user_id"] == 1
    assert data["artist_id"] == 5
    assert data["status"] == STATUS_DONE


# ---------- create_request + next_request_id ----------

def test_next_request_id_empty() -> None:
    """Для пустой коллекции следующий id = 1."""
    assert next_request_id([]) == 1


def test_next_request_id_non_empty() -> None:
    """Для непустой — max(id) + 1."""
    user = User(1, "Иван", "ivan@example.com")
    requests = [
        Request(1, user, "A"),
        Request(5, user, "B"),
        Request(3, user, "C"),
    ]
    assert next_request_id(requests) == 6


def test_create_request_appends() -> None:
    """create_request добавляет заявку в коллекцию."""
    user = User(1, "Иван", "ivan@example.com")
    requests: list[Request] = []
    request = create_request(requests, 1, user, "Miyagi", city="Москва")
    assert len(requests) == 1
    assert requests[0] is request
    assert request.city == "Москва"


# ---------- выборки ----------

def test_find_request_by_id_found() -> None:
    """Найти заявку по ID."""
    user = User(1, "Иван", "ivan@example.com")
    requests = [
        Request(1, user, "Miyagi"),
        Request(2, user, "NF"),
    ]
    result = find_request_by_id(requests, 2)
    assert result is not None
    assert result.query == "NF"


def test_find_request_by_id_not_found() -> None:
    """Заявка по ID не найдена."""
    user = User(1, "Иван", "ivan@example.com")
    requests = [Request(1, user, "Miyagi")]
    assert find_request_by_id(requests, 99) is None


def test_get_user_requests() -> None:
    """Заявки только одного пользователя."""
    user_a = User(1, "A", "a@a")
    user_b = User(2, "B", "b@b")
    requests = [
        Request(1, user_a, "Miyagi"),
        Request(2, user_b, "NF"),
        Request(3, user_a, "Andy Panda"),
    ]
    result = get_user_requests(requests, user_a)
    assert len(result) == 2
    assert {r.id for r in result} == {1, 3}


def test_get_active_requests() -> None:
    """Только активные заявки (new или in_progress)."""
    user = User(1, "Иван", "ivan@example.com")
    r1 = Request(1, user, "A")           # new
    r2 = Request(2, user, "B")           # in_progress
    r3 = Request(3, user, "C")           # cancelled
    r4 = Request(4, user, "D")           # done
    r2.take_in_work()
    r3.cancel()
    r4.complete(Artist(1, "Miyagi", "Россия"))

    active = get_active_requests([r1, r2, r3, r4])
    assert len(active) == 2
    assert {r.id for r in active} == {1, 2}
