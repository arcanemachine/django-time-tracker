from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.shortcuts import render

from . import serializers
from accounts.models import TimerUser
from tracker.models import Activity, Timer


class UserList(generics.ListAPIView):
    serializer_class = serializers.TimerUserSerializer
    queryset = TimerUser.objects.all() 


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TimerUserSerializer
    queryset = TimerUser.objects.all() 
    lookup_url_kwarg = 'user_pk'


class ActivityList(generics.ListCreateAPIView):
    serializer_class = serializers.ActivitySerializer
    queryset = Activity.objects.all() 


class ActivityDetail(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'activity_pk'
    serializer_class = serializers.ActivitySerializer
    queryset = Activity.objects.all() 


class TimerList(generics.ListCreateAPIView):
    serializer_class = serializers.TimerSerializer
    queryset = Timer.objects.all() 


class TimerDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = serializers.TimerSerializer
    queryset = Timer.objects.all() 
    lookup_url_kwarg = 'timer_pk'

@api_view(['POST'])
def create_timer(request, user_pk, activity_pk):
    newest_timer = Timer.objects.filter(activity__pk=activity_pk)
    if newest_timer.exists() and newest_timer.last().stop_time is None:
        return Response({
            "message": "Please stop your last timer before making a new one."})
    else:
        timer = Timer.objects.create(activity__pk=activity_pk)
        return response({
            "id": timer.pk,
            "message": f"New {timer.activity.name} timer started",
            })
