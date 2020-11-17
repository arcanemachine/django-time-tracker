from django.db import models
from django.utils import timezone

class Activity(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'activities'

    def __str__(self):
        return self.name

class Timer(models.Model):
    activity = models.ForeignKey('Activity', on_delete=models.CASCADE)

    start_timestamp = models.DateTimeField(default=timezone.now)
    stop_timestamp = models.DateTimeField(blank=True, null=True)
    pause_timestamp = models.DateTimeField(blank=True, null=True)
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

    def get_run_time(self):
        return self.get_formatted_time(self.run_seconds)

    def get_pause_time(self):
        return self.get_formatted_time(self.pause_seconds)

    def __str__(self):
        current_state = "running"
        if self.is_paused:
            current_state = "paused"
        if self.stop_timestamp:
            current_state = "stopped"
        return f"{self.activity.name} - "\
               f"{self.get_run_time()} ({current_state})"
