from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.wine_list, name="wine_cellar"),  # Corrected to call wine_list
]
