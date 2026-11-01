import os
import sys
import sqlite3
import django
from pathlib import Path

# 1. Настройка путей и окружения Django
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "music_service.settings")

# 2. Инициализация Django (ОБЯЗАТЕЛЬНО до импорта моделей!)
django.setup()

# 3. Импорт моделей (СТРОГО ПОСЛЕ django.setup())
from songs.models import Song
from user_requests.models import User, Request
from artists.models import Artist
from labels.models import Label

# Путь к базе данных из ПР7
SOURCE_DB = BASE_DIR / "data" / "music_service.sqlite"


def import_data():
    if not SOURCE_DB.exists():
        print(f"Старая база не найдена по пути: {SOURCE_DB}")
        return

    with sqlite3.connect(SOURCE_DB) as conn:
        conn.row_factory = sqlite3.Row

        # 1. Перенос Лейблов
        labels_data = conn.execute("SELECT * FROM labels").fetchall()
        for row in labels_data:
            Label.objects.update_or_create(
                id=row['id'],
                defaults={
                    'name': row['name'],
                    'founded_year': row['founded_year'],
                    'country': row['country']
                }
            )
        print(f"Перенесено лейблов: {len(labels_data)}")

        # 2. Перенос Артистов
        artists_data = conn.execute("SELECT * FROM artists").fetchall()
        for row in artists_data:
            Artist.objects.update_or_create(
                id=row['id'],
                defaults={
                    'name': row['name'],
                    'country': row['country'],
                    'label_id': row['label_id']
                }
            )
        print(f"Перенесено артистов: {len(artists_data)}")

        # 3. Перенос Пользователей
        users_data = conn.execute("SELECT * FROM users").fetchall()
        for row in users_data:
            User.objects.update_or_create(
                id=row['id'],
                defaults={
                    'name': row['name'],
                    'email': row['email'],
                    'city': row['city']
                }
            )
        print(f"Перенесено пользователей: {len(users_data)}")

        # 4. Перенос Песен
        songs_data = conn.execute("SELECT * FROM songs").fetchall()
        for row in songs_data:
            Song.objects.update_or_create(
                id=row['id'],
                defaults={
                    'title': row['title'],
                    'artist_id': row['artist_id'],
                    'genre': row['genre'],
                    'release_year': row['release_year'],
                    'duration_sec': row['duration_sec'],
                    'has_lyrics': bool(row['has_lyrics'])
                }
            )
        print(f"Перенесено песен: {len(songs_data)}")

        # 5. Перенос Заявок
        requests_data = conn.execute("SELECT * FROM requests").fetchall()
        for row in requests_data:
            Request.objects.update_or_create(
                id=row['id'],
                defaults={
                    'user_id': row['user_id'],
                    'query': row['query'],
                    'genre': row['genre'],
                    'city': row['city'],
                    'status': row['status'],
                    'created_at': row['created_at'],
                    'found_artist_id': row['artist_id']
                }
            )
        print(f"Перенесено заявок: {len(requests_data)}")

    print("Импорт завершен успешно!")


if __name__ == "__main__":
    import_data()
