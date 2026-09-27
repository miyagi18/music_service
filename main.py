"""Консольный интерфейс сервиса поиска музыкальных коллективов."""
from models import Artist, Label, Request, Song, User
from models.artists import (
    find_artist_by_name,
    find_artists_for_request,
    get_artists_by_label,
)
from models.labels import find_label_by_name
from models.requests import (
    create_request,
    find_request_by_id,
    get_user_requests,
    next_request_id,
)
from models.songs import find_song_by_title, get_songs_by_artist
from models.users import find_user_by_id, find_user_by_name
from storage import (
    load_artists,
    load_labels,
    load_requests,
    load_songs,
    load_users,
    save_artists,
    save_labels,
    save_requests,
    save_songs,
    save_users,
)

DATA = "data"


# ---------- вывод ----------

def print_song_info(song: Song) -> None:
    lyrics = (
        "текст доступен" if song.has_lyrics
        else "текст не доступен"
    )
    print(
        f"  • {song.title} ({song.release_year}) — "
        f"{song.genre}. {lyrics}"
    )


def print_artist_info(artist: Artist) -> None:
    print(f"  • {artist}")


def print_request_info(request: Request) -> None:
    print(f"  • {request}")


# ---------- пользовательские сценарии ----------

def search_song(songs: list[Song]) -> None:
    query = input("Введите название песни: ").strip()
    found = find_song_by_title(songs, query)
    if not found:
        print("Песни не найдены.")
        return
    print(f"\nНайдено песен: {len(found)}")
    for song in found:
        print_song_info(song)


def search_artist(
    artists: list[Artist], songs: list[Song]
) -> None:
    query = input("Введите имя артиста: ").strip()
    found = find_artist_by_name(artists, query)
    if not found:
        print("Артист не найден.")
        return
    for artist in found:
        print(f"\nАртист: {artist}")
        artist_songs = get_songs_by_artist(songs, artist)
        if artist_songs:
            print("Дискография:")
            for song in artist_songs:
                print_song_info(song)
        else:
            print("  Песен в базе нет.")


def search_label(
    labels: list[Label],
    artists: list[Artist],
) -> None:
    query = input("Введите название лейбла: ").strip()
    found = find_label_by_name(labels, query)
    if not found:
        print("Лейбл не найден.")
        return
    for label in found:
        print(f"\nЛейбл: {label}")
        label_artists = get_artists_by_label(artists, label)
        if label_artists:
            print(f"Артисты на лейбле ({len(label_artists)}):")
            for artist in label_artists:
                print_artist_info(artist)
        else:
            print("  На этом лейбле пока нет артистов в базе.")


def create_user_request(
    users: list[User],
    artists: list[Artist],
    requests: list[Request],
) -> None:
    """Сценарий создания заявки от пользователя."""\

    user: User | None = None

    name = input("Введите имя пользователя: ").strip()
    found_users = find_user_by_name(users, name)
    if not found_users:
        print("Пользователь не найден.")
        return

    if len(found_users) == 1:
        user = found_users[0]
    else:
        for u in found_users:
            print(f"  id={u.id}: {u}")
        user_id = input("Уточните id пользователя: ").strip()
        if not user_id.isdigit():
            print("Некорректный id.")
            return
        user = find_user_by_id(users, int(user_id))
        if user is None:
            print("Пользователь не найден.")
            return

    print(f"\nПользователь: {user}")
    query = input("Что ищем (название коллектива): ").strip()
    genre = input("Желаемый жанр (можно пусто): ").strip()
    city = input("Город / страна (можно пусто): ").strip()

    request = create_request(
        requests=requests,
        request_id=next_request_id(requests),
        user=user,
        query=query,
        genre=genre,
        city=city,
    )

    print(f"\nЗаявка #{request.id} создана.")
    matches = find_artists_for_request(artists, query, city)
    if matches:
        print(f"Подходящие коллективы ({len(matches)}):")
        for artist in matches:
            print_artist_info(artist)
    else:
        print("Подходящих коллективов пока не найдено.")


def list_requests(
    requests: list[Request],
    users: list[User],
) -> None:
    """Показать заявки (все или конкретного пользователя)."""
    mode = input(
        "Показать все заявки (1) или заявки пользователя (2)? "
    ).strip()
    if mode == "2":
        name = input("Введите имя пользователя: ").strip()
        found_users = find_user_by_name(users, name)
        if not found_users:
            print("Пользователь не найден.")
            return
        user = found_users[0]
        requests_to_show = get_user_requests(requests, user)
    else:
        requests_to_show = requests

    if not requests_to_show:
        print("Заявок нет.")
        return
    print(f"\nЗаявок: {len(requests_to_show)}")
    for request in requests_to_show:
        print_request_info(request)


def process_request(
    requests: list[Request],
    artists: list[Artist],
) -> None:
    """Обработать заявку: назначить найденный коллектив или отменить."""
    raw_id = input("Введите id заявки: ").strip()
    if not raw_id.isdigit():
        print("Некорректный id.")
        return
    request = find_request_by_id(requests, int(raw_id))
    if request is None:
        print("Заявка не найдена.")
        return

    print(f"\n{request}")
    print("1. Назначить коллектив")
    print("2. Отменить заявку")
    print("0. Назад")
    action = input("Выберите действие: ").strip()

    if action == "1":
        query = input("Имя коллектива для назначения: ").strip()
        matches = find_artists_for_request(
            artists, query, request.city
        )
        if not matches:
            print("Коллектив не найден.")
            return
        for i, artist in enumerate(matches, start=1):
            print(f"  {i}. {artist}")
        choice = input("Выберите номер: ").strip()
        if not choice.isdigit() or not (1 <= int(choice) <= len(matches)):
            print("Некорректный выбор.")
            return
        request.complete(matches[int(choice) - 1])
        print(f"Заявка #{request.id} закрыта.")
    elif action == "2":
        request.cancel()
        print(f"Заявка #{request.id} отменена.")


# ---------- главное меню ----------

def main() -> None:
    labels = load_labels(f"{DATA}/labels.json")
    artists = load_artists(f"{DATA}/artists.json", labels)
    songs = load_songs(f"{DATA}/songs.json", artists)
    users = load_users(f"{DATA}/users.json")
    requests = load_requests(
        f"{DATA}/requests.json", users, artists
    )

    while True:
        print("\n--- Меню ---")
        print("1. Поиск песни")
        print("2. Поиск артиста и его песен")
        print("3. Поиск лейбла и его артистов")
        print("4. Оставить заявку на поиск коллектива")
        print("5. Просмотр заявок")
        print("6. Обработать заявку")
        print("0. Выход")

        raw = input("Выберите действие: ").strip()
        if not raw.isdigit():
            print("Ошибка: нужно ввести число.")
            continue
        choice = int(raw)

        if choice == 1:
            search_song(songs)
        elif choice == 2:
            search_artist(artists, songs)
        elif choice == 3:
            search_label(labels, artists)
        elif choice == 4:
            create_user_request(users, artists, requests)
        elif choice == 5:
            list_requests(requests, users)
        elif choice == 6:
            process_request(requests, artists)
        elif choice == 0:
            break
        else:
            print("Неверный пункт меню.")

    # сохраняем изменения
    save_labels(f"{DATA}/labels.json", labels)
    save_artists(f"{DATA}/artists.json", artists)
    save_songs(f"{DATA}/songs.json", songs)
    save_users(f"{DATA}/users.json", users)
    save_requests(f"{DATA}/requests.json", requests)
    print("Данные сохранены. Выход.")


if __name__ == "__main__":
    main()
