from django.conf import settings
from django.db import models
from django.utils import timezone


class Activity(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'activities'

    def __str__(self):
        return self.name

#class TodayTimerManager(models.Manager):
#    def get_queryset(self):
#


class Timer(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    activity = models.ForeignKey(
        'Activity', default=1, on_delete=models.CASCADE)

    start_time = models.DateTimeField()
    stop_time = models.DateTimeField(blank=True, null=True)
    last_update_time = models.DateTimeField(blank=True, null=True)
    run_seconds = models.IntegerField(default=0)
    pause_seconds = models.IntegerField(default=0)

    is_paused = models.BooleanField(default=False)

    def get_seconds(self, elapsed_seconds):
        return int(elapsed_seconds)

    def get_formatted_seconds(self, elapsed_seconds):
        return str(int(elapsed_seconds % 60)).zfill(2)

    def get_minutes(self, elapsed_seconds):
        return int(elapsed_seconds / 60)

    def get_formatted_minutes(self, elapsed_seconds):
        return str(int((elapsed_seconds / 60) % 60)).zfill(2)

    def get_hours(self, elapsed_seconds):
        return int(elapsed_seconds / 3600)

    def get_formatted_hours(self, elapsed_seconds):
        return str(int(self.get_hours(elapsed_seconds) % 24)).zfill(2)

    def get_days(self, elapsed_seconds):
        return int(elapsed_seconds / 86_400)

    def get_formatted_days(self, elapsed_seconds):
        days = int(elapsed_seconds / 86_400)
        if days:
            return f"{str(days).zfill(2)}d "
        else:
            return ""

    def get_formatted_time(self, elapsed_seconds):
        days = self.get_formatted_days(elapsed_seconds)
        hours = self.get_formatted_hours(elapsed_seconds)
        minutes = self.get_formatted_minutes(elapsed_seconds)
        seconds = self.get_formatted_seconds(elapsed_seconds)
        return f"{days}{hours}:{minutes}:{seconds}"

    def get_time_since_last_update(self):
        current_time = timezone.now()
        if self.stop_time:
            return None
        elif self.last_update_time:
            return self.get_formatted_time(
                (current_time - self.last_update_time).total_seconds())
        else:
            return self.get_formatted_time(
                (current_time - self.start_time).total_seconds())

    def get_run_time(self, formatted=True):
        current_time = timezone.now()
        if not self.last_update_time:
            return self.get_formatted_time(
                (current_time - self.start_time).total_seconds())
        elif self.is_paused:
            return self.get_formatted_time(self.run_seconds)
        else:
            seconds_since_timer_resumed = \
                (current_time - self.last_update_time).total_seconds()
            return self.get_formatted_time(
                self.run_seconds + seconds_since_timer_resumed)

    def get_pause_time(self, formatted=True):
        current_time = timezone.now()
        if self.is_paused:
            return self.get_formatted_time(
                (current_time - self.last_update_time).total_seconds())
        else:
            return self.get_formatted_time(self.pause_seconds)

    def get_timer_state(self):
        time_since_last_update = self.get_time_since_last_update()
        current_state = f"current run time: {time_since_last_update}"
        if self.is_paused:
            current_state = f"current pause time: {time_since_last_update}"
        if self.stop_time:
            current_state = "stopped"
        return current_state

    def pause(self):
        self.is_paused = True

        if not self.last_update_time:
            current_time = timezone.now()
            elapsed_time = \
                (current_time - self.start_time).total_seconds()
        elif self.last_update_time:
            current_time = timezone.now()
            elapsed_time = \
                (current_time - self.last_update_time).total_seconds()

        self.run_seconds += elapsed_time
        self.last_update_time = current_time
        self.save()

    def stop(self):
        self.last_update_time = timezone.now()
        self.stop_time = self.last_update_time
        self.save()

    def resume(self):
        if not self.is_paused:
            return None

        current_time = timezone.now()
        elapsed_time = (current_time - self.last_update_time).total_seconds()

        self.pause_seconds += elapsed_time
        self.last_update_time = current_time
        self.is_paused = False
        self.save()

    def __str__(self):
        return f"{self.activity.name} - "\
            f"Running: {self.get_run_time()}, "\
            f"Paused: {self.get_pause_time()}, "\
            f"({self.get_timer_state()})"

    def save(self, *args, **kwargs):
        self.start_time = timezone.now()
        super().save(*args, **kwargs)
