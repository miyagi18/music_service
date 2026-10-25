"""Страницы песен: список, карточка и статистика."""
from django.http import Http404
from django.shortcuts import render
from db.database import get_connection


def songs(request):
    """Список всех песен."""
    conn = get_connection()
    songs_data = conn.execute("""
        SELECT songs.id, songs.title, songs.genre, songs.release_year,
               artists.name AS artist_name
        FROM songs
        JOIN artists ON songs.artist_id = artists.id
        ORDER BY songs.title
    """).fetchall()
    conn.close()
    return render(request, "songs/list.html", {"songs": songs_data})


def song_detail(request, song_id: int):
    """Карточка песни."""
    conn = get_connection()
    song = conn.execute("""
        SELECT songs.id, songs.title, songs.genre, songs.release_year,
               songs.duration_sec, songs.has_lyrics,
               artists.id AS artist_id, artists.name AS artist_name
        FROM songs
        JOIN artists ON songs.artist_id = artists.id
        WHERE songs.id = ?
    """, [song_id]).fetchone()
    conn.close()

    if song is None:
        raise Http404("Песня не найдена")
    return render(request, "songs/detail.html", {"song": song})


def statistics(request):
    """Статистика песен по артистам (GROUP BY)."""
    conn = get_connection()
    stats = conn.execute("""
        SELECT artists.name AS artist_name,
               COUNT(songs.id) AS songs_count
        FROM artists
        LEFT JOIN songs ON artists.id = songs.artist_id
        GROUP BY artists.id, artists.name
        ORDER BY songs_count DESC
    """).fetchall()
    conn.close()
    return render(request, "songs/statistics.html", {"stats": stats})
