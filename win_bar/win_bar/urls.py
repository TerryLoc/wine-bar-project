from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views  #


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="winery"),  # Home view for the main page
    path("wine_cellar/", include("bookings.urls")),  # Include URLs for the bookings app
    path(
        "register/", auth_views.LoginView.as_view(), name="register"
    ),  # Login view for the registration page
]
