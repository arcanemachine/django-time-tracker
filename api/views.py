from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

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


class TimerCreate(APIView):
    serializer_class = serializers.TimerSerializer

    def get(self, request, *args, **kwargs):
        activity = get_object_or_404(Activity, pk=self.kwargs['activity_pk'])
        timers = Timer.objects.filter(activity=activity)

        if timers.exists() and timers.last().stop_time is None:
            return Response({
                "message":
                    "Please stop your last timer before starting a new one."})
        else:
            timer = Timer.objects.create(activity=activity)
            return Response({
                "id": timer.pk,
                "message": f"New '{timer.activity.name}' timer started"})


class TimerPause(APIView):
    serializer_class = serializers.TimerSerializer

    def get(self, request, *args, **kwargs):
        activity = get_object_or_404(Activity, pk=self.kwargs['activity_pk'])
        timers = Timer.objects.filter(activity=activity)

        if timers.exists() and timers.last().stop_time is None:
            return Response({
                "message":
                    "Please stop your last timer before starting a new one."})
        else:
            timer = Timer.objects.create(activity=activity)
            return Response({
                "id": timer.pk,
                "message": f"New '{timer.activity.name}' timer started"})
