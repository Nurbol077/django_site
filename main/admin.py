from django.contrib import admin

from .models import Player


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("jersey_number", "last_name", "first_name", "position", "club")
    list_display_links = ("jersey_number", "last_name")
    list_filter = ("position", "club")
    search_fields = ("first_name", "last_name", "club", "nationality")
    ordering = ("club", "jersey_number")
    fieldsets = (
        ("Основные сведения", {
            "fields": ("first_name", "last_name", "jersey_number", "position", "club", "photo")
        }),
        ("Профиль", {"fields": ("birth_date", "nationality", "height_cm", "weight_kg")} ),
        ("Статистика", {"fields": ("appearances", "goals", "assists")} ),
    )
