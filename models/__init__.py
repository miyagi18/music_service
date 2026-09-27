"""Пакет моделей предметной области музыкального сервиса."""
from .labels import Label
from .artists import Artist
from .songs import Song
from .users import User
from .requests import Request

__all__ = ["Label", "Artist", "Song", "User", "Request"]
