"""Загрузка и сохранение данных: JSON ↔ объекты предметной области."""
import json
from typing import Any, List

from models import Artist, Label, Request, Song, User


def _load_raw(filename: str) -> list[dict[str, Any]]:
    try:
        with open(filename, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Файл {filename} не найден.")
        return []
    except json.JSONDecodeError:
        print(f"Файл {filename} содержит некорректный JSON.")
        return []


def _save_raw(filename: str, data: list[dict[str, Any]]) -> None:
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


# ---------- labels ----------

def load_labels(filename: str) -> List[Label]:
    return [Label.from_data(item) for item in _load_raw(filename)]


def save_labels(filename: str, labels: List[Label]) -> None:
    _save_raw(filename, [label.to_dict() for label in labels])


# ---------- artists ----------

def load_artists(
    filename: str, labels: List[Label]
) -> List[Artist]:
    return [
        Artist.from_data(item, labels)
        for item in _load_raw(filename)
    ]


def save_artists(filename: str, artists: List[Artist]) -> None:
    _save_raw(filename, [artist.to_dict() for artist in artists])


# ---------- songs ----------

def load_songs(
    filename: str, artists: List[Artist]
) -> List[Song]:
    songs: List[Song] = []
    for item in _load_raw(filename):
        song = Song.from_data(item, artists)
        if song is not None:
            songs.append(song)
    return songs


def save_songs(filename: str, songs: List[Song]) -> None:
    _save_raw(filename, [song.to_dict() for song in songs])


# ---------- users ----------

def load_users(filename: str) -> List[User]:
    return [User.from_data(item) for item in _load_raw(filename)]


def save_users(filename: str, users: List[User]) -> None:
    _save_raw(filename, [user.to_dict() for user in users])


# ---------- requests ----------

def load_requests(
    filename: str,
    users: List[User],
    artists: List[Artist],
) -> List[Request]:
    result: List[Request] = []
    for item in _load_raw(filename):
        request = Request.from_data(item, users, artists)
        if request is not None:
            result.append(request)
    return result


def save_requests(filename: str, requests: List[Request]) -> None:
    _save_raw(filename, [r.to_dict() for r in requests])
