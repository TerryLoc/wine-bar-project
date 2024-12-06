from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = "bookings"

urlpatterns = [
    path("wine_cellar/", views.wine_list, name="wine_cellar"),
    path("book/<int:wine_id>/", views.book_wine, name="book"),
    path("register/", views.register, name="register"),
    path(
        "login/", LoginView.as_view(template_name="bookings/login.html"), name="login"
    ),
    path("profile/", views.profile, name="profile"),
]
