from django.contrib import admin
from .models import Song


@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "artist", "release_year",
                    "duration_sec", "is_long")
    list_display_links = ("title",)
    search_fields = ("title", "artist__name")
    list_filter = ("genre", "release_year", "has_lyrics")
    ordering = ("-release_year",)
    list_select_related = ("artist",)
