from datetime import datetime

song_title = "Bismarck"
song_genre = "Hip-Hop"
song_release_year_str = "2018"  

label_name = "Hajime Records"
label_founded_year = 2015
label_country = "Russia"

current_year = datetime.now().year

def add_song(song_title, genre, year_release):
    release_year = int(year_release)

    if song_title == "":
        return 'Необходимо указать название песни'
    if release_year > current_year:
        return 'Год песни не может быть больше текущего года'
    if genre == "":
        return 'Жанр песни необходимо выбрать' 
    return f'Песня успешно создана. \n Название: {song_title} \n Жанр: {genre} \n Год выпуска: {year_release}'

def filter_song_by_era(title, year_release, era_start):
    era_end = era_start + 9
    if int(year_release) >= era_start and int(year_release) < era_end:
        return f'Песня {title} попадает в эпоху {era_start}'
    else:
        return f'Песня {title} не относится к эпохе {era_start}'

def get_label_info(title, year):
    if current_year < year:
        return f'Ошибка: год указан некорректно'
    if current_year - year >= 20:
        return f'Лейбл {title} старый'
    elif current_year - year <= 5:
        return f'Лейбл {title} молодой'
    else:
        return f'Лейбл активно развивается'

print(add_song(song_title, song_genre, song_release_year_str))
print(filter_song_by_era(song_title, song_release_year_str, 2010))
print(get_label_info(label_name, label_founded_year))


    

