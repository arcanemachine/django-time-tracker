from rest_framework import generics
from django.shortcuts import render

from . import serializers
from tracker.models import Activity, Timer


class ActivityList(generics.ListCreateAPIView):
    serializer_class = serializers.ActivitySerializer
    queryset = Activity.objects.all() 


class TimerList(generics.ListCreateAPIView):
    serializer_class = serializers.TimerSerializer
    queryset = Timer.objects.all() 
