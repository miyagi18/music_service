import json
from db.database import get_connection


def load_json(filename):
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def import_all():
    conn = get_connection()
    try:
        # 1. Лейблы
        labels = load_json("data/labels.json")
        conn.executemany(
            """
            INSERT INTO labels (id, name, founded_year, country)
            VALUES (?, ?, ?, ?)
            """,
            [
                (label["id"], label["name"],
                 label["founded_year"], label["country"])
                for label in labels
            ]
        )
        # 2. Артисты
        artists = load_json("data/artists.json")
        conn.executemany(
            """
            INSERT INTO artists (id, name, country, label_id)
            VALUES (?, ?, ?, ?)
            """,
            [
                (artist["id"], artist["name"],
                 artist["country"], artist["label_id"])
                for artist in artists
            ]
        )
        # 3. Пользователи
        users = load_json("data/users.json")
        conn.executemany(
            """
            INSERT INTO users (id, name, email, city)
            VALUES (?, ?, ?, ?)
            """,
            [
                (user["id"], user["name"],
                 user["email"], user.get("city", ""))
                for user in users
            ]
        )
        # 4. Песни
        songs = load_json("data/songs.json")
        conn.executemany(
            """
            INSERT INTO songs (
                id, title, artist_id, genre,
                release_year, duration_sec, has_lyrics
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (song["id"], song["title"], song["artist_id"],
                 song["genre"], song["release_year"],
                 song["duration_sec"], int(song.get("has_lyrics", False)))
                for song in songs
            ]
        )
        # 5. Заявки
        requests = load_json("data/requests.json")
        conn.executemany(
            """
            INSERT INTO requests (
                id, user_id, query, genre,
                city, status, created_at, artist_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            [
                (req["id"], req["user_id"], req["query"],
                 req.get("genre", ""), req.get("city", ""),
                 req["status"], req.get("created_at", ""),
                 req.get("artist_id"))
                for req in requests
            ]
        )
        conn.commit()
        print("Данные успешно импортированы!")
    except Exception as e:
        conn.rollback()
        print(f"Ошибка импорта: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    import_all()
