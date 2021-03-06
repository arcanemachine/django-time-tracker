from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularRedocView

from . import views

urlpatterns = [
    path('', views.hello_world, name='root'),
    path('csv/', views.csv_download, name='csv_download'),
    path('csv/<int:timer_pk>/', views.csv_download, name='csv_download_item'),
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/redoc/',
         SpectacularRedocView.as_view(url_name='schema'),
         name='redoc'),
]
