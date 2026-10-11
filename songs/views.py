from django.http import HttpResponse


def songs(request):
    return HttpResponse("Список песен")


def song_detail(request, song_id):
    return HttpResponse(f"Песня {song_id}")