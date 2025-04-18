from django.contrib import admin
from django.urls import path, include
from . import views  # Ensure this contains a 'home' view
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


# URL patterns for the winery app and the bookings app
urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="winery"),  # Home page
    path("wine_cellar/", include("bookings.urls")),  # Routes to bookings app
    path(
        "logout/", auth_views.LogoutView.as_view(next_page="winery"), name="logout"
    ),  # Logout
]
# If the project is in debug mode, add the media URL and document root
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Custom error handlers
handler404 = "win_bar.views.custom_page_not_found"
