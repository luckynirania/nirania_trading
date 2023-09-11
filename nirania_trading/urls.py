from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/univest/", include("univest.urls")),
    path("api/v1/angel_broking/", include("angel_broking.urls")),
]
