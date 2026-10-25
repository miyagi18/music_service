"""Страницы заявок на поиск музыкального коллектива."""
from django.http import Http404
from django.shortcuts import render
from db.database import get_connection
from models.requests import STATUS_LABELS


def _format_requests(rows):
    """Добавляем читаемый статус к результатам SQL."""
    result = []
    for row in rows:
        req_dict = dict(row)
        status = req_dict["status"]
        req_dict["status_display"] = STATUS_LABELS.get(status, status)
        result.append(req_dict)
    return result


def requests_list(request):
    """Список всех заявок."""
    conn = get_connection()
    rows = conn.execute("""
        SELECT requests.id, requests.query, requests.status,
               users.name AS user_name
        FROM requests
        JOIN users ON requests.user_id = users.id
        ORDER BY requests.created_at DESC
    """).fetchall()
    conn.close()
    return render(
        request,
        "user_requests/list.html",
        {"requests": _format_requests(rows)}
    )


def request_detail(request, request_id: int):
    """Карточка отдельной заявки."""
    conn = get_connection()
    row = conn.execute("""
        SELECT requests.id, requests.query, requests.genre,
               requests.city, requests.status, requests.created_at,
               users.name AS user_name,
               artists.id AS found_artist_id,
               artists.name AS found_artist_name
        FROM requests
        JOIN users ON requests.user_id = users.id
        LEFT JOIN artists ON requests.artist_id = artists.id
        WHERE requests.id = ?
    """, [request_id]).fetchone()
    conn.close()

    if row is None:
        raise Http404("Заявка не найдена")

    req_formatted = _format_requests([row])[0]
    return render(
        request,
        "user_requests/detail.html",
        {"req": req_formatted}
    )
