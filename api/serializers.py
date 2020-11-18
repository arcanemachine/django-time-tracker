from rest_framework import serializers

from tracker.models import Activity, Timer


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
