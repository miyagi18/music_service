"""Страницы песен: список и карточка."""
from django.http import Http404
from django.shortcuts import render

from models.songs import find_song_by_id
from storage import load_artists, load_labels, load_songs

DATA_LABELS = "data/labels.json"
DATA_ARTISTS = "data/artists.json"
DATA_SONGS = "data/songs.json"


def _load_all_songs():
    """Загрузить песни со связанными артистами и лейблами."""
    labels_list = load_labels(DATA_LABELS)
    artists_list = load_artists(DATA_ARTISTS, labels_list)
    return load_songs(DATA_SONGS, artists_list)


def songs(request):
    """Список всех песен."""
    songs_list = _load_all_songs()
    return render(request, "songs/list.html", {
        "songs": songs_list,
    })


def song_detail(request, song_id: int):
    """Карточка песни."""
    songs_list = _load_all_songs()
    song = find_song_by_id(songs_list, song_id)
    if song is None:
        raise Http404("Песня не найдена")
    return render(request, "songs/detail.html", {"song": song})
