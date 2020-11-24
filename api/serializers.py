from rest_framework import serializers

from accounts.models import TimerUser
from tracker.models import Activity, Timer


class TimerUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimerUser
        fields = ['id', 'username', 'timezone']
        read_only_fields = ['username']

    def to_representation(self, instance):
        return {'id': instance.id,
                'username': instance.username,
                'timezone': instance.timezone.zone}


class ActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Activity
        fields = ['id', 'name']


class TimerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Timer
        fields = ['id', 'activity', 'start_time', 'stop_time',
                  'last_update_time', 'run_seconds', 'pause_seconds',
                  'is_running']
        read_only_fields = [
            'activity', 'start_time', 'stop_time', 'last_update_time',
            'run_seconds', 'pause_seconds', 'is_running']

    def to_representation(self, instance):

        def get_unix_time(time):
            return int(time.timestamp()) if time else None

        formatted_start_time = get_unix_time(self.instance.start_time)
        formatted_stop_time = get_unix_time(self.instance.stop_time)
        formatted_last_update_time = \
            get_unix_time(self.instance.last_update_time)

        return {'id': instance.id,
                'activity': instance.activity.pk,
                'start_time': formatted_start_time,
                'stop_time': formatted_stop_time,
                'last_update_time': formatted_last_update_time,
                'run_seconds': instance.run_seconds,
                'pause_seconds': instance.pause_seconds,
                'is_running': instance.is_running}
