from django.shortcuts import render, get_object_or_404
from django.db.models import Count, F
from django.db.models import Count, Q 
from django.core.paginator import Paginator
from songs.models import Song
from artists.models import Artist


def songs(request):
    # Базовый запрос
    songs_qs = Song.objects.select_related('artist').all()

    # 1. Поиск (по названию песни, имени артиста или году)
    query = request.GET.get('q', '').strip()
    if query:
        # Ищем совпадения по трем полям через логическое ИЛИ (|)
        q_obj = Q(title__icontains=query) | Q(artist__name__icontains=query)
        
        # Если ввели число, ищем еще и по году выпуска
        if query.isdigit():
            q_obj |= Q(release_year=int(query))
            
        songs_qs = songs_qs.filter(q_obj)

    # 2. Сортировка (безопасная, через словарь)
    sort = request.GET.get('sort', 'title')
    sort_fields = {
        'title': 'title', 
        'year': '-release_year', 
        'artist': 'artist__name'
    }
    sort_field = sort_fields.get(sort, 'title')
    songs_qs = songs_qs.order_by(sort_field)

    # 3. Пагинация (по 5 песен на страницу)
    paginator = Paginator(songs_qs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "songs": page_obj,
        "page_obj": page_obj,
        "query": query,
        "sort": sort,
    }
    return render(request, "songs/list.html", context)


def song_detail(request, song_id: int):
    song = get_object_or_404(Song.objects.select_related('artist'), pk=song_id)
    return render(request, "songs/detail.html", {"song": song})


def statistics(request):
    # Аннотация (annotate) и агрегация (Count)
    stats = Artist.objects.annotate(
        songs_count=Count('songs')
    ).order_by('-songs_count')

    return render(request, "songs/statistics.html", {"stats": stats})
