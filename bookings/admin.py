from django.contrib import admin
from .models import Booking, WineCellar, UserProfile


#  Register the models with the admin site to manage them through the admin interface
class WineCellarAdmin(admin.ModelAdmin):
    list_display = ("title", "date", "available_spots", "total_spots")
    search_fields = ("title",)
    list_filter = ("date",)


#  Register the models with the admin site to manage them through the admin interface
class BookingAdmin(admin.ModelAdmin):
    list_display = ("user", "wine_experience", "spots_reserved", "timestamp")
    search_fields = ("user__username", "wine_experience__title")
    list_filter = ("wine_experience", "timestamp")


# Register the models with the admin site to manage them through the admin interface
admin.site.register(WineCellar, WineCellarAdmin)
admin.site.register(Booking, BookingAdmin)
admin.site.register(UserProfile)
