from django.contrib import admin
from .models import wineCellar


@admin.register(wineCellar)
class WineCellarAdmin(admin.ModelAdmin):
    list_display = ("title", "price", "date", "available_spots")
    search_fields = ("title", "description")
    list_filter = ("date",)
    fields = (
        "title",
        "description",
        "price",
        "date",
        "available_spots",
        "what_to_expect",
        "join_us",
    )  # Include new fields
