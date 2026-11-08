from django.contrib import admin
from .models import Label


@admin.register(Label)
class LabelAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "country", "founded_year")
    search_fields = ("name",)
    list_filter = ("country",)
    ordering = ("name",)
    list_per_page = 10
