from django.urls import path
from . import views

app_name = "bookings"

urlpatterns = [
    path("", views.wine_list, name="wine_cellar"),
    path("book/<int:wine_id>/", views.book_wine, name="book"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("profile/", views.profile, name="profile"),
]
