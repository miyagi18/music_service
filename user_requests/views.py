"""Страницы заявок на поиск музыкального коллектива."""
from django.http import Http404
from django.shortcuts import render

from models.requests import STATUS_LABELS, find_request_by_id
from storage import load_artists, load_labels, load_requests, load_users

DATA_LABELS = "data/labels.json"
DATA_ARTISTS = "data/artists.json"
DATA_USERS = "data/users.json"
DATA_REQUESTS = "data/requests.json"


def _load_all_requests():
    """Загрузить заявки со связанными пользователями и артистами."""
    labels_list = load_labels(DATA_LABELS)
    artists_list = load_artists(DATA_ARTISTS, labels_list)
    users_list = load_users(DATA_USERS)
    requests_list = load_requests(
        DATA_REQUESTS, users_list, artists_list
    )
    # Добавляем каждому объекту читаемую подпись статуса
    for req in requests_list:
        req.status_display = STATUS_LABELS.get(req.status, req.status)
    return requests_list


def requests_list(request):
    """Список всех заявок."""
    requests_list_ = _load_all_requests()
    return render(request, "user_requests/list.html", {
        "requests": requests_list_,
    })


def request_detail(request, request_id: int):
    """Карточка отдельной заявки."""
    requests_list_ = _load_all_requests()
    req = find_request_by_id(requests_list_, request_id)
    if req is None:
        raise Http404("Заявка не найдена")
    return render(request, "user_requests/detail.html", {"req": req})
