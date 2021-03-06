import pytz
from datetime import datetime
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
        fields = ['id',
                  'activity',
                  'start_time',
                  'stop_time',
                  'last_update_time',
                  'run_seconds',
                  'pause_seconds',
                  'is_running']

    def to_internal_value(self, data):
        UTC = pytz.timezone('UTC')
        if data.get('start_time', None):
            data['start_time'] = \
                datetime.utcfromtimestamp(data['start_time']).astimezone(UTC)
        if data.get('stop_time', None):
            data['stop_time'] = \
                datetime.utcfromtimestamp(data['stop_time']).astimezone(UTC)
        if data.get('last_update_time', None):
            data['last_update_time'] = \
                datetime.utcfromtimestamp(
                    data['last_update_time']).astimezone(UTC)
        return data

    def to_representation(self, instance):

        def get_unix_time(time):
            return int(time.timestamp()) if time else None

        formatted_start_time = get_unix_time(instance.start_time)
        formatted_stop_time = get_unix_time(instance.stop_time)
        formatted_last_update_time = get_unix_time(instance.last_update_time)

        return {'id': instance.id,
                'activity': instance.activity.pk,
                'start_time': formatted_start_time,
                'stop_time': formatted_stop_time,
                'last_update_time': formatted_last_update_time,
                'run_seconds': instance.run_seconds,
                'pause_seconds': instance.pause_seconds,
                'is_running': instance.is_running}
