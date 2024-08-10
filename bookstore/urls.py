from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from rest_framework import permissions # type: ignore

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]