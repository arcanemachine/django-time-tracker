from rest_framework import serializers

from accounts.models import TimerUser
from tracker.models import Activity, Timer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimerUser
        fields = ['id', 'username', 'timezone']


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'name']


class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timer
        fields = ['id', 'activity', 'start_timestamp', 'stop_timestamp',
                  'pause_timestamp', 'run_seconds', 'pause_seconds',
                  'is_paused']
