from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404

from . import serializers
from accounts.models import TimerUser
from tracker.models import Activity, Timer

class PingPongView(generics.GenericAPIView):
    serializer_class = None

    def get(self, request, *args, **kwargs):
        return Response({"message": "Pong!"})

    def post(self, request, *args, **kwargs):
        return Response({"message": f"You said 'f{request.POST['message']}'"})


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
        running_timer = Timer.objects.filter(activity=activity)

        if running_timer.exists() and running_timer.last().stop_time is None:
            return Response({
                "id": running_timer.pk,
                "status_code": "fail",
                "message":
                    "Please stop the previous timer first."})
        else:
            timer = Timer.objects.create(activity=activity)
            return Response({
                "id": timer.pk,
                "status_code": "success",
                "message": f"New '{timer.activity.name}' timer started"})


class TimerPause(generics.GenericAPIView):
    serializer_class = serializers.TimerSerializer

    def get(self, request, *args, **kwargs):
        self.timer = self.get_object()
        if self.timer.is_stopped():
            return Response({
                "id": self.timer.id,
                "status_code": "fail",
                "message": "This timer has already been stopped."})
        if self.timer.is_paused():
            return Response({
                "id": self.timer.id,
                "status_code": "fail",
                "message": "This timer is already paused."})
        else:
            self.timer.pause()
            return Response({
                "id": self.timer.id,
                "status_code": "success",
                "message": "Timer paused"})

    def get_object(self):
        return Timer.objects.get(pk=self.kwargs['timer_pk'])


class TimerResume(generics.GenericAPIView):
    serializer_class = serializers.TimerSerializer

    def get(self, request, *args, **kwargs):
        self.timer = self.get_object()
        if self.timer.is_running:
            return Response({
                "id": self.timer.id,
                "status_code": "fail",
                "message": "This timer is already running."})
        elif self.timer.is_paused() or self.timer.is_stopped():
            self.timer.resume()
            return Response({
                "id": self.timer.id,
                "status_code": "success",
                "message": "Timer resumed"})

    def get_object(self):
        return Timer.objects.get(pk=self.kwargs['timer_pk'])


class TimerStop(generics.GenericAPIView):
    serializer_class = serializers.TimerSerializer

    def get(self, request, *args, **kwargs):
        self.timer = self.get_object()
        if self.timer.is_stopped():
            return Response({
                "id": self.timer.id,
                "status_code": "fail",
                "message": "This timer is already stopped."})
        elif self.timer.is_running or self.timer.is_paused():
            self.timer.stop()
            return Response({
                "id": self.timer.id,
                "status_code": "success",
                "message": "Timer stopped"})

    def get_object(self):
        return Timer.objects.get(pk=self.kwargs['timer_pk'])
