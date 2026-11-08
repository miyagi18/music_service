from songs.models import Song
from artists.models import Artist


def global_stats(request):
    """Передает общее количество артистов и песен во все шаблоны."""
    return {
        "global_artist_count": Artist.objects.count(),
        "global_song_count": Song.objects.count(),
    }
