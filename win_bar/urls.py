from django.contrib import admin
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="winery"),
    path("wine_cellar/", include("bookings.urls")),
    path("register/", auth_views.LoginView.as_view(), name="register"),
    path(
        "logout/", auth_views.LogoutView.as_view(next_page="winery"), name="logout"
    ),  # Logout view
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
