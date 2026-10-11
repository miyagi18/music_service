"""Тесты модели Label и функций поиска лейблов."""
from models import Label
from models.labels import find_label_by_id, find_label_by_name


# ---------- создание объекта ----------

def test_label_creation() -> None:
    """Создание объекта Label и его атрибутов."""
    label = Label(1, "Hajime Records", 2017, "Россия")
    assert label.id == 1
    assert label.name == "Hajime Records"
    assert label.founded_year == 2017
    assert label.country == "Россия"


def test_label_str() -> None:
    """Строковое представление лейбла."""
    label = Label(1, "Hajime Records", 2017, "Россия")
    text = str(label)
    assert "Hajime Records" in text
    assert "Россия" in text
    assert "2017" in text


# ---------- from_data / to_dict ----------

def test_label_from_data() -> None:
    """Создание лейбла из словаря."""
    data = {
        "id": 2,
        "name": "Capitol CMG",
        "founded_year": 2014,
        "country": "США",
    }
    label = Label.from_data(data)
    assert label.id == 2
    assert label.name == "Capitol CMG"
    assert label.country == "США"


def test_label_to_dict() -> None:
    """Сериализация лейбла в словарь."""
    label = Label(1, "Hajime Records", 2017, "Россия")
    data = label.to_dict()
    assert data == {
        "id": 1,
        "name": "Hajime Records",
        "founded_year": 2017,
        "country": "Россия",
    }


def test_label_roundtrip() -> None:
    """Проверка: from_data(to_dict()) даёт тот же лейбл."""
    original = Label(1, "Hajime Records", 2017, "Россия")
    restored = Label.from_data(original.to_dict())
    assert restored.id == original.id
    assert restored.name == original.name
    assert restored.founded_year == original.founded_year
    assert restored.country == original.country


# ---------- поиск ----------

def test_find_label_by_name_case_insensitive() -> None:
    """Поиск лейбла по названию без учёта регистра."""
    labels = [
        Label(1, "Hajime Records", 2017, "Россия"),
        Label(2, "Capitol CMG", 2014, "США"),
    ]
    result = find_label_by_name(labels, "hajime")
    assert len(result) == 1
    assert result[0].name == "Hajime Records"


def test_find_label_by_name_partial() -> None:
    """Поиск лейбла по частичному вхождению."""
    labels = [
        Label(1, "Hajime Records", 2017, "Россия"),
        Label(2, "Capitol CMG", 2014, "США"),
    ]
    result = find_label_by_name(labels, "cap")
    assert len(result) == 1
    assert result[0].id == 2


def test_find_label_not_found() -> None:
    """Поиск лейбла, которого нет в базе."""
    labels = [Label(1, "Hajime Records", 2017, "Россия")]
    assert find_label_by_name(labels, "unknown") == []


def test_find_label_by_id_found() -> None:
    """Поиск лейбла по ID — найден."""
    labels = [
        Label(1, "Hajime Records", 2017, "Россия"),
        Label(2, "Capitol CMG", 2014, "США"),
    ]
    result = find_label_by_id(labels, 2)
    assert result is not None
    assert result.name == "Capitol CMG"


def test_find_label_by_id_not_found() -> None:
    """Поиск лейбла по ID — не найден."""
    labels = [Label(1, "Hajime Records", 2017, "Россия")]
    assert find_label_by_id(labels, 99) is None
