"""Тесты модели Song и функций поиска песен."""
from models import Artist, Label, Song
from models.songs import (
    find_song_by_title,
    get_songs_by_artist,
    get_songs_by_label,
)


# ---------- создание объекта ----------

def test_song_creation() -> None:
    """Создание песни и её атрибутов."""
    artist = Artist(1, "Miyagi", "Россия")
    song = Song(2, "Колизей", artist, "Hip-Hop", 2017, 268, True)
    assert song.id == 2
    assert song.title == "Колизей"
    assert song.artist is artist
    assert song.genre == "Hip-Hop"
    assert song.release_year == 2017
    assert song.duration_sec == 268
    assert song.has_lyrics is True


def test_song_str_with_lyrics() -> None:
    """Строка песни — текст доступен."""
    artist = Artist(1, "Miyagi", "Россия")
    song = Song(2, "Колизей", artist, "Hip-Hop", 2017, 268, True)
    text = str(song)
    assert "Колизей" in text
    assert "Miyagi" in text
    assert "текст доступен" in text


def test_song_str_without_lyrics() -> None:
    """Строка песни — текста нет."""
    artist = Artist(1, "Эндшпиль", "Россия")
    song = Song(1, "Bismarck", artist, "Hip-Hop", 2018, 215, False)
    assert "текст не доступен" in str(song)


# ---------- from_data / to_dict ----------

def test_song_from_data_links_artist() -> None:
    """from_data подтягивает объект Artist."""
    artists = [Artist(2, "Эндшпиль", "Россия")]
    data = {
        "id": 1,
        "title": "Bismarck",
        "artist_id": 2,
        "genre": "Hip-Hop",
        "release_year": 2018,
        "duration_sec": 215,
    }
    song = Song.from_data(data, artists)
    assert song is not None
    assert song.artist.id == 2
    assert song.artist.name == "Эндшпиль"


def test_song_from_data_artist_not_found() -> None:
    """Если артист не найден — возвращается None."""
    artists: list[Artist] = []
    data = {
        "id": 1,
        "title": "Bismarck",
        "artist_id": 99,
        "genre": "Hip-Hop",
        "release_year": 2018,
        "duration_sec": 215,
    }
    assert Song.from_data(data, artists) is None


def test_song_to_dict_stores_artist_id() -> None:
    """to_dict хранит artist_id, а не объект."""
    artist = Artist(2, "Эндшпиль", "Россия")
    song = Song(1, "Bismarck", artist, "Hip-Hop", 2018, 215)
    data = song.to_dict()
    assert data["artist_id"] == 2
    assert data["title"] == "Bismarck"


# ---------- поиск ----------

def test_find_song_by_title_case_insensitive() -> None:
    """Поиск песни без учёта регистра."""
    artist = Artist(2, "Эндшпиль", "Россия")
    songs = [Song(1, "Bismarck", artist, "Hip-Hop", 2018, 215)]
    result = find_song_by_title(songs, "bismarck")
    assert len(result) == 1
    assert result[0].title == "Bismarck"


def test_find_song_by_title_russian() -> None:
    """Поиск песни с кириллицей."""
    artist = Artist(1, "Miyagi", "Россия")
    songs = [Song(2, "Колизей", artist, "Hip-Hop", 2017, 268)]
    result = find_song_by_title(songs, "колизей")
    assert len(result) == 1


def test_find_song_not_found() -> None:
    """Песня не найдена."""
    artist = Artist(1, "Miyagi", "Россия")
    songs = [Song(2, "Колизей", artist, "Hip-Hop", 2017, 268)]
    assert find_song_by_title(songs, "Unknown") == []


def test_get_songs_by_artist() -> None:
    """Дискография артиста."""
    a1 = Artist(1, "Miyagi", "Россия")
    a2 = Artist(2, "Эндшпиль", "Россия")
    songs = [
        Song(1, "Bismarck", a2, "Hip-Hop", 2018, 215),
        Song(2, "Колизей", a1, "Hip-Hop", 2017, 268),
        Song(3, "Самурай", a1, "Hip-Hop", 2017, 165),
    ]
    result = get_songs_by_artist(songs, a1)
    assert len(result) == 2
    titles = {s.title for s in result}
    assert titles == {"Колизей", "Самурай"}


def test_get_songs_by_artist_empty() -> None:
    """У артиста нет песен в базе."""
    a1 = Artist(1, "Miyagi", "Россия")
    a2 = Artist(2, "Эндшпиль", "Россия")
    songs = [Song(1, "Bismarck", a2, "Hip-Hop", 2018, 215)]
    assert get_songs_by_artist(songs, a1) == []


def test_get_songs_by_label() -> None:
    """Дискография всех артистов лейбла."""
    label = Label(1, "Hajime Records", 2017, "Россия")
    a1 = Artist(1, "Miyagi", "Россия", label)
    a2 = Artist(2, "Эндшпиль", "Россия", label)
    a3 = Artist(10, "NF", "США")  # без лейбла
    songs = [
        Song(1, "Bismarck", a2, "Hip-Hop", 2018, 215),
        Song(2, "Колизей", a1, "Hip-Hop", 2017, 268),
        Song(15, "Let You Down", a3, "Hip-Hop", 2017, 212),
    ]
    result = get_songs_by_label(songs, [a1, a2, a3], label.id)
    assert len(result) == 2
    assert {s.title for s in result} == {"Bismarck", "Колизей"}
