from django.urls import path
from . import views
from django.contrib.auth.views import LoginView

# Define the app name to refer to the app in the project
app_name = "bookings"

# Define the URL patterns for the app
urlpatterns = [
    path("", views.wine_list, name="wine_cellar"),
    path("book/<int:wine_id>/", views.book_wine, name="book"),
    path("register/", views.register, name="register"),
    # Use the custom login view to handle user authentication
    path(
        "login/",
        views.CustomLoginView.as_view(template_name="bookings/login.html"),
        name="login",
    ),
    path("profile/", views.profile, name="profile"),
    path("cancel_booking/", views.cancel_booking, name="cancel_booking"),
]
