from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from django.views.static import serve

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("shop.urls")),
    # Uploaded fabric photos live on the Render persistent disk. Django serves
    # them directly, which is fine for a small shop; move to S3/Cloudinary if
    # traffic grows.
    path("media/<path:path>", serve, {"document_root": settings.MEDIA_ROOT}),
]
