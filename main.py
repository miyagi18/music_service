from storage import load_json
from songs import find_song_by_title, get_songs_by_artist
from artists import find_artist_by_name, get_artists_by_label
from labels import find_label_by_name

def print_song_info(song: dict) -> None:
    lyrics_status = "Текст доступен" if song.get('has_lyrics') else "Текст не доступен"
    print(f"{song['title']} ({song['release_year']}) - {song['genre']}")
    print(f"Текст песни: {lyrics_status}")

def main() -> None:
    songs = load_json('data/songs.json')
    artists = load_json('data/artists.json')
    labels = load_json('data/labels.json')

    while True:
        print("\n--- Меню ---")
        print("1. Поиск песни")
        print("2. Поиск артиста и его песен")
        print("3. Поиск лейбла и его артистов")
        print("0. Выход")

        try:
            choice = int(input("Выберите действие: "))
        except ValueError:
            print("Ошибка: Нужно ввести число!")
            continue

        if choice == 1:
            query = input("Введите название песни: ")
            found_songs = find_song_by_title(songs, query)
            if found_songs:
                print(f"\nНайдено песен: {len(found_songs)}")
                for s in found_songs:
                    print_song_info(s)
            else:
                print("Песни не найдены.")

        elif choice == 2:
            query = input("Введите имя артиста: ")
            found_artists = find_artist_by_name(artists, query)
            if found_artists:
                for artist in found_artists:
                    print(f"\nАртист: {artist['name']}")
                    artist_songs = get_songs_by_artist(songs, artist['id'])
                    if artist_songs:
                        print("   Дискография:")
                        for s in artist_songs:
                            print_song_info(s)
                    else:
                        print("Песен в базе нет.")
            else:
                print("Артист не найден.")

        elif choice == 3:
            query = input("Введите название лейбла: ")
            found_labels = find_label_by_name(labels, query)
            if found_labels:
                for label in found_labels:
                    print(f"\nЛейбл: {label['name']} ({label['country']})")
                    label_artists = get_artists_by_label(artists, label['id'])
                    if label_artists:
                        print(f"Артисты на лейбле ({len(label_artists)}):")
                        for artist in label_artists:
                            print(f"{artist['name']}")
                    else:
                        print("   На этом лейбле пока нет артистов в базе.")
            else:
                print("Лейбл не найден.")

        elif choice == 0:
            print("Выход из программы...")
            break
        else:
            print("Неверный пункт меню.")

if __name__ == "__main__":
    main()