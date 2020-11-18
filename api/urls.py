from django.urls import path

from . import views

app_name = 'api'

urlpatterns = [
    path('users/',
         views.UserList.as_view(),
         name='user_list'),
    path('users/<int:user_pk>/',
         views.UserDetail.as_view(),
         name='user_detail'),
    path('users/<int:user_pk>/activities/',
         views.ActivityDetail.as_view(),
         name='activity_list'),
    path('users/<int:user_pk>/activities/<int:activity_pk>/',
         views.ActivityDetail.as_view(),
         name='activity_detail'),
    path('users/<int:user_pk>/activities/<int:activity_pk>/timers/',
         views.TimerList.as_view(),
         name='timer_list'),
    path('users/<int:user_pk>/activities/<int:activity_pk>/timers/'
         '<int:timer_pk>/',
         views.TimerDetail.as_view(),
         name='timer_detail'),
]
