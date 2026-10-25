"""Страницы лейблов: список и карточка."""
from django.http import Http404
from django.shortcuts import render
from db.database import get_connection


def labels(request):
    """Список всех лейблов."""
    conn = get_connection()
    labels_data = conn.execute("""
        SELECT id, name, founded_year, country
        FROM labels
        ORDER BY name
    """).fetchall()
    conn.close()
    return render(request, "labels/list.html", {"labels": labels_data})


def label_detail(request, label_id: int):
    """Карточка лейбла и артисты этого лейбла."""
    conn = get_connection()

    label = conn.execute("""
        SELECT id, name, founded_year, country
        FROM labels
        WHERE id = ?
    """, [label_id]).fetchone()

    if label is None:
        conn.close()
        raise Http404("Лейбл не найден")

    artists = conn.execute("""
        SELECT id, name, country
        FROM artists
        WHERE label_id = ?
        ORDER BY name
    """, [label_id]).fetchall()

    conn.close()
    return render(
        request,
        "labels/detail.html",
        {"label": label, "artists": artists}
    )
