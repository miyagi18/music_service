"""Страницы артистов: список и карточка с дискографией."""
from django.http import Http404
from django.shortcuts import render

from models.artists import get_artist_by_id
from models.songs import get_songs_by_artist
from storage import load_artists, load_labels, load_songs

DATA_LABELS = "data/labels.json"
DATA_ARTISTS = "data/artists.json"
DATA_SONGS = "data/songs.json"


def artists(request):
    """Список всех артистов."""
    labels_list = load_labels(DATA_LABELS)
    artists_list = load_artists(DATA_ARTISTS, labels_list)
    return render(request, "artists/list.html", {
        "artists": artists_list,
    })


def artist_detail(request, artist_id: int):
    """Карточка артиста с его дискографией."""
    labels_list = load_labels(DATA_LABELS)
    artists_list = load_artists(DATA_ARTISTS, labels_list)
    artist = get_artist_by_id(artists_list, artist_id)
    if artist is None:
        raise Http404("Артист не найден")

    songs_list = load_songs(DATA_SONGS, artists_list)
    songs = get_songs_by_artist(songs_list, artist)

    return render(request, "artists/detail.html", {
        "artist": artist,
        "songs": songs,
    })
