from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularRedocView

urlpatterns = [
    path('admin/',
         admin.site.urls),
    path('api/v1/',
         include('api.urls')),
    path('api/schema/',
         SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),
]
