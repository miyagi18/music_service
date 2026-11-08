from django.contrib import admin
from .models import Artist
from songs.models import Song

# Встраиваем песни прямо в карточку артиста (Inline)


class SongInline(admin.TabularInline):
    model = Song
    extra = 0
    fields = ("title", "release_year", "genre")


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country", "label")
    list_display_links = ("name",)
    # Поиск по связанному полю label__name
    search_fields = ("name", "label__name")
    list_filter = ("country", "label")
    ordering = ("name",)
    # Оптимизация запросов для списка
    list_select_related = ("label",)
    inlines = (SongInline,)
