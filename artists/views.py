from django.shortcuts import render, get_object_or_404
from artists.models import Artist


def artists(request):
    # select_related("label") делает JOIN сразу (оптимизация запросов)
    artists_list = Artist.objects.select_related(
        'label').all().order_by('name')
    return render(request, "artists/list.html", {"artists": artists_list})


def artist_detail(request, artist_id: int):
    artist = get_object_or_404(
        Artist.objects.select_related('label'), pk=artist_id)
    # related_name='songs' позволяет получить все песни артиста
    songs = artist.songs.all().order_by('-release_year')
    return render(request, "artists/detail.html", {"artist": artist, "songs": songs})
