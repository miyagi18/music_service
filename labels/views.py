"""Страницы лейблов: список и карточка."""
from django.http import Http404
from django.shortcuts import render

from models.artists import get_artists_by_label
from models.labels import find_label_by_id
from storage import load_artists, load_labels

DATA_LABELS = "data/labels.json"
DATA_ARTISTS = "data/artists.json"


def labels(request):
    """Список всех лейблов из JSON."""
    labels_list = load_labels(DATA_LABELS)
    return render(request, "labels/list.html", {
        "labels": labels_list,
    })


def label_detail(request, label_id: int):
    """Карточка лейбла и артисты этого лейбла."""
    labels_list = load_labels(DATA_LABELS)
    label = find_label_by_id(labels_list, label_id)
    if label is None:
        raise Http404("Лейбл не найден")

    artists_list = load_artists(DATA_ARTISTS, labels_list)
    label_artists = get_artists_by_label(artists_list, label)

    return render(request, "labels/detail.html", {
        "label": label,
        "artists": label_artists,
    })