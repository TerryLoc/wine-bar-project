# urls.py (main)

from django.contrib import admin
from django.urls import path, include
from . import views  # Ensure views.py exists with a 'home' view defined
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.home, name="winery"),  # Ensure views.home is defined
    path("wine_cellar/", include("bookings.urls")),  # Redirect to app URLs
    path("logout/", auth_views.LogoutView.as_view(next_page="winery"), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
