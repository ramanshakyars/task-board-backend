from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    re_path(r"^api/auth/", include("accounts.urls")),
    re_path(r"^api/tasks", include("tasks.urls")),
    re_path(r"^api/comments", include("comments.urls")),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
