"""Тесты модели Artist и функций поиска артистов."""
from models import Artist, Label
from models.artists import (
    find_artist_by_name,
    find_artists_for_request,
    get_artist_by_id,
    get_artists_by_label,
)


# ---------- создание объекта ----------

def test_artist_creation() -> None:
    """Создание артиста с лейблом."""
    label = Label(1, "Hajime Records", 2017, "Россия")
    artist = Artist(1, "Miyagi", "Россия", label)
    assert artist.id == 1
    assert artist.name == "Miyagi"
    assert artist.country == "Россия"
    assert artist.label is label


def test_artist_without_label() -> None:
    """Артист без лейбла — связь None."""
    artist = Artist(1, "Independent", "Россия")
    assert artist.label is None


def test_artist_str_with_label() -> None:
    """Строка артиста содержит название лейбла."""
    label = Label(1, "Hajime Records", 2017, "Россия")
    artist = Artist(1, "Miyagi", "Россия", label)
    text = str(artist)
    assert "Miyagi" in text
    assert "Hajime Records" in text


def test_artist_str_without_label() -> None:
    """Строка артиста без лейбла содержит пометку."""
    artist = Artist(1, "Independent", "Россия")
    assert "без лейбла" in str(artist)


# ---------- from_data / to_dict ----------

def test_artist_from_data_links_label() -> None:
    """from_data подтягивает объект Label по label_id."""
    labels = [
        Label(1, "Hajime Records", 2017, "Россия"),
        Label(2, "Capitol CMG", 2014, "США"),
    ]
    data = {"id": 1, "name": "Miyagi", "country": "Россия", "label_id": 1}
    artist = Artist.from_data(data, labels)
    assert artist.label is not None
    assert artist.label.id == 1
    assert artist.label.name == "Hajime Records"


def test_artist_from_data_without_label() -> None:
    """Если label_id не найден — label остаётся None."""
    labels = [Label(2, "Capitol CMG", 2014, "США")]
    data = {"id": 1, "name": "Miyagi", "country": "Россия", "label_id": 1}
    artist = Artist.from_data(data, labels)
    assert artist.label is None


def test_artist_to_dict_stores_label_id() -> None:
    """to_dict сохраняет именно id лейбла, а не объект."""
    label = Label(1, "Hajime Records", 2017, "Россия")
    artist = Artist(1, "Miyagi", "Россия", label)
    data = artist.to_dict()
    assert data["label_id"] == 1
    assert isinstance(data["label_id"], int)


def test_artist_to_dict_without_label() -> None:
    """У артиста без лейбла label_id = None."""
    artist = Artist(1, "Independent", "Россия")
    assert artist.to_dict()["label_id"] is None


# ---------- поиск ----------

def test_find_artist_by_name_case_insensitive() -> None:
    """Поиск артиста по имени без учёта регистра."""
    artists = [
        Artist(1, "Miyagi", "Россия"),
        Artist(2, "Эндшпиль", "Россия"),
    ]
    result = find_artist_by_name(artists, "miyagi")
    assert len(result) == 1
    assert result[0].name == "Miyagi"


def test_find_artist_by_name_not_found() -> None:
    """Поиск артиста, которого нет в базе."""
    artists = [Artist(1, "Miyagi", "Россия")]
    assert find_artist_by_name(artists, "Unknown") == []


def test_get_artist_by_id_found() -> None:
    """Найти артиста по ID."""
    artists = [
        Artist(1, "Miyagi", "Россия"),
        Artist(2, "Эндшпиль", "Россия"),
    ]
    result = get_artist_by_id(artists, 2)
    assert result is not None
    assert result.name == "Эндшпиль"


def test_get_artist_by_id_not_found() -> None:
    """Поиск артиста по ID — не найден."""
    artists = [Artist(1, "Miyagi", "Россия")]
    assert get_artist_by_id(artists, 99) is None


# ---------- обратная сторона связи «лейбл → артисты» ----------

def test_get_artists_by_label() -> None:
    """Получение списка артистов лейбла."""
    label_1 = Label(1, "Hajime Records", 2017, "Россия")
    label_2 = Label(2, "Capitol CMG", 2014, "США")
    artists = [
        Artist(1, "Miyagi", "Россия", label_1),
        Artist(2, "Эндшпиль", "Россия", label_1),
        Artist(10, "NF", "США", label_2),
    ]
    result = get_artists_by_label(artists, label_1)
    assert len(result) == 2
    names = {a.name for a in result}
    assert names == {"Miyagi", "Эндшпиль"}


def test_get_artists_by_label_empty() -> None:
    """У лейбла нет артистов — пустой список."""
    label = Label(3, "Empty Records", 2020, "Россия")
    artists = [Artist(1, "Miyagi", "Россия")]
    assert get_artists_by_label(artists, label) == []


# ---------- подбор артистов под заявку ----------

def test_find_artists_for_request_by_name() -> None:
    """Подбор по названию коллектива."""
    artists = [
        Artist(1, "Miyagi", "Россия"),
        Artist(2, "Эндшпиль", "Россия"),
    ]
    result = find_artists_for_request(artists, "miyagi")
    assert len(result) == 1
    assert result[0].name == "Miyagi"


def test_find_artists_for_request_by_city() -> None:
    """Подбор по стране/городу."""
    artists = [
        Artist(1, "Miyagi", "Россия"),
        Artist(10, "NF", "США"),
    ]
    result = find_artists_for_request(artists, "", "сша")
    assert len(result) == 1
    assert result[0].name == "NF"


def test_find_artists_for_request_no_match() -> None:
    """Подбор не нашёл никого."""
    artists = [Artist(1, "Miyagi", "Россия")]
    assert find_artists_for_request(artists, "unknown", "Антарктида") == []
