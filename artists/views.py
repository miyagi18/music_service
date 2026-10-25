"""Страницы артистов: список и карточка с дискографией."""
from django.http import Http404
from django.shortcuts import render
from db.database import get_connection


def artists(request):
    """Список всех артистов."""
    conn = get_connection()
    artists_data = conn.execute("""
        SELECT artists.id, artists.name, artists.country,
               labels.name AS label_name
        FROM artists
        LEFT JOIN labels ON artists.label_id = labels.id
        ORDER BY artists.name
    """).fetchall()
    conn.close()
    return render(request, "artists/list.html", {"artists": artists_data})


def artist_detail(request, artist_id: int):
    """Карточка артиста с его дискографией."""
    conn = get_connection()
    artist = conn.execute("""
        SELECT artists.id, artists.name, artists.country,
               labels.id AS label_id, labels.name AS label_name
        FROM artists
        LEFT JOIN labels ON artists.label_id = labels.id
        WHERE artists.id = ?
    """, [artist_id]).fetchone()

    if artist is None:
        conn.close()
        raise Http404("Артист не найден")

    songs = conn.execute("""
        SELECT id, title, genre, release_year, duration_sec, has_lyrics
        FROM songs
        WHERE artist_id = ?
        ORDER BY release_year DESC
    """, [artist_id]).fetchall()

    conn.close()
    return render(
        request,
        "artists/detail.html",
        {"artist": artist, "songs": songs}
    )
