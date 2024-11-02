from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

app_name = "bookings"

urlpatterns = [
    path("", views.wine_list, name="wine_cellar"),
    path("book/<int:wine_id>/", views.book_wine, name="book"),
    path("register/", views.register, name="register"),
    path("login/", views.login_view, name="login"),
    path("profile/", views.profile, name="profile"),
    path("logout/", LogoutView.as_view(next_page="winery"), name="logout"),
    # Profile page (for viewing profile info)
]
