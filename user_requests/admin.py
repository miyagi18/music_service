from django.contrib import admin
from .models import User, Request


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "email", "city")
    search_fields = ("name", "email")


class RequestInline(admin.TabularInline):
    model = Request
    extra = 0
    fields = ("query", "status", "created_at")


@admin.register(Request)
class RequestAdmin(admin.ModelAdmin):
    list_display = ("id", "query", "user", "status", "created_at")
    list_display_links = ("id", "query")
    search_fields = ("query", "user__name")
    list_filter = ("status", "created_at")
    ordering = ("-created_at",)
    list_select_related = ("user",)
