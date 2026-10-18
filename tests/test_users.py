"""Тесты модели User и функций поиска пользователей."""
from models import User
from models.users import find_user_by_id, find_user_by_name


# ---------- создание объекта ----------

def test_user_creation() -> None:
    """Создание пользователя и его атрибутов."""
    user = User(1, "Иван Петров", "ivan@example.com", "Москва")
    assert user.id == 1
    assert user.name == "Иван Петров"
    assert user.email == "ivan@example.com"
    assert user.city == "Москва"


def test_user_without_city() -> None:
    """Город необязателен — по умолчанию пустая строка."""
    user = User(1, "Иван", "ivan@example.com")
    assert user.city == ""


def test_user_str() -> None:
    """Строковое представление содержит имя, email и город."""
    user = User(1, "Иван Петров", "ivan@example.com", "Москва")
    text = str(user)
    assert "Иван Петров" in text
    assert "ivan@example.com" in text
    assert "Москва" in text


# ---------- from_data / to_dict ----------

def test_user_from_data() -> None:
    """Создание пользователя из словаря с city."""
    data = {
        "id": 2,
        "name": "Анна Смирнова",
        "email": "anna@example.com",
        "city": "Санкт-Петербург",
    }
    user = User.from_data(data)
    assert user.id == 2
    assert user.name == "Анна Смирнова"
    assert user.email == "anna@example.com"
    assert user.city == "Санкт-Петербург"


def test_user_from_data_without_city() -> None:
    """Если city в JSON нет — поле остаётся пустым."""
    data = {"id": 1, "name": "Иван", "email": "ivan@example.com"}
    user = User.from_data(data)
    assert user.city == ""


def test_user_to_dict() -> None:
    """Сериализация в словарь."""
    user = User(1, "Иван", "ivan@example.com", "Москва")
    assert user.to_dict() == {
        "id": 1,
        "name": "Иван",
        "email": "ivan@example.com",
        "city": "Москва",
    }


def test_user_to_dict_without_city() -> None:
    """to_dict корректно сохраняет пустой город."""
    user = User(1, "Иван", "ivan@example.com")
    data = user.to_dict()
    assert data["city"] == ""


def test_user_roundtrip() -> None:
    """from_data(to_dict()) даёт тот же объект."""
    original = User(1, "Иван", "ivan@example.com", "Москва")
    restored = User.from_data(original.to_dict())
    assert restored.id == original.id
    assert restored.name == original.name
    assert restored.email == original.email
    assert restored.city == original.city


# ---------- поиск по ID ----------

def test_find_user_by_id_found() -> None:
    """Найти пользователя по ID."""
    users = [
        User(1, "Иван", "ivan@example.com"),
        User(2, "Анна", "anna@example.com"),
    ]
    result = find_user_by_id(users, 2)
    assert result is not None
    assert result.name == "Анна"
    assert result.id == 2


def test_find_user_by_id_not_found() -> None:
    """Пользователь с таким ID отсутствует — None."""
    users = [User(1, "Иван", "ivan@example.com")]
    assert find_user_by_id(users, 99) is None


def test_find_user_by_id_empty_list() -> None:
    """В пустой коллекции никого не найти."""
    assert find_user_by_id([], 1) is None


# ---------- поиск по имени ----------

def test_find_user_by_name_case_insensitive() -> None:
    """Поиск без учёта регистра."""
    users = [
        User(1, "Иван Петров", "ivan@example.com"),
        User(2, "Анна Смирнова", "anna@example.com"),
    ]
    result = find_user_by_name(users, "иван")
    assert len(result) == 1
    assert result[0].id == 1


def test_find_user_by_name_uppercase() -> None:
    """Верхний регистр в запросе тоже работает."""
    users = [User(1, "Иван", "ivan@example.com")]
    result = find_user_by_name(users, "ИВАН")
    assert len(result) == 1


def test_find_user_by_name_partial() -> None:
    """Частичное совпадение по имени."""
    users = [
        User(1, "Иван Петров", "ivan1@example.com"),
        User(2, "Иван Иванов", "ivan2@example.com"),
        User(3, "Анна Смирнова", "anna@example.com"),
    ]
    result = find_user_by_name(users, "иван")
    assert len(result) == 2
    assert {u.id for u in result} == {1, 2}


def test_find_user_by_name_not_found() -> None:
    """Пользователь не найден — пустой список."""
    users = [User(1, "Иван", "ivan@example.com")]
    assert find_user_by_name(users, "Пётр") == []


def test_find_user_by_name_empty_list() -> None:
    """Пустая коллекция — пустой результат."""
    assert find_user_by_name([], "Иван") == []
