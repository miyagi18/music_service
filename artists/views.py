from django.shortcuts import render, get_object_or_404
from artists.models import Artist


def artists(request):
    # select_related('label') делает JOIN, чтобы не делать лишний запрос к БД
    artists_list = Artist.objects.select_related(
        'label').all().order_by('name')
    return render(request, "artists/list.html", {"artists": artists_list})


def artist_detail(request, slug):
    # Ищем по slug вместо id
    artist = get_object_or_404(
        Artist.objects.select_related('label'), slug=slug)
    songs = artist.songs.all().order_by('-release_year')
    return render(request, "artists/detail.html", {"artist": artist, "songs": songs})
