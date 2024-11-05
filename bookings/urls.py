from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

app_name = "bookings"

urlpatterns = [
    path("", views.wine_list, name="wine_cellar"),  # Main page of wine list
    path("book/<int:wine_id>/", views.book_wine, name="book"),
    path("register/", views.register, name="register"),
    path(
        "login/", LoginView.as_view(template_name="bookings/login.html"), name="login"
    ),  # Use LoginView for login
    path("profile/", views.profile, name="profile"),
]
