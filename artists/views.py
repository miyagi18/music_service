from django.http import HttpResponse


def artists(request):
    return HttpResponse("Список артистов")


def artist_detail(request, artist_id):
    return HttpResponse(f"Артист {artist_id}")