from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/", include("accounts.api.urls")),
    path("dutches/", include("dutches.api.urls")),
    path("splits/", include("spliter.api.urls")),
]
