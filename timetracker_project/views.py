import csv
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from tracker.models import Timer

def hello_world(request):
    return HttpResponse('Hello world!')

def csv_download(request, timer_pk=None):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="timer_data.csv"'

    if timer_pk:
        timer = get_object_or_404(Timer, pk=timer_pk)
        timers = Timer.objects.filter(pk=timer.pk)
    else:
        timers = Timer.objects.all()

    writer = csv.writer(response)

    writer.writerow(
        ['activity.name', 'start_time', 'stop_time', 'last_update_time',
        'run_seconds', 'pause_seconds', 'is_running'])

    for timer in timers:
        writer.writerow(
            [timer.activity.name, timer.start_time, timer.stop_time,
            timer.last_update_time, timer.run_seconds, timer.pause_seconds,
            timer.is_running])

    return response
