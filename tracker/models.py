from django.conf import settings
from django.db import models
from django.utils import timezone

current_time = timezone.now


class Activity(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name_plural = 'activities'

    def __str__(self):
        return self.name


class Timer(models.Model):
    activity = models.ForeignKey(
        'Activity', default=1, on_delete=models.CASCADE)

    start_time = models.DateTimeField(blank=True, null=True)
    stop_time = models.DateTimeField(blank=True, null=True)
    last_update_time = models.DateTimeField(blank=True, null=True)
    run_seconds = models.IntegerField(default=0, blank=True, null=True)
    pause_seconds = models.IntegerField(default=0, blank=True, null=True)

    is_running = models.BooleanField(default=True)
    is_tamper_proof = models.BooleanField(default=False)

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

    def get_localized_time(self, time):
        user = self.activity.user
        if user and user.timezone:
            return time.astimezone(user.timezone)
        else:
            return time

    def get_days(self, elapsed_seconds):
        return int(elapsed_seconds / 86_400)

    def get_formatted_days(self, elapsed_seconds):
        days = self.get_days(elapsed_seconds)
        return f"{str(days).zfill(2)}"

    def get_formatted_time(self, elapsed_seconds):
        days = self.get_formatted_days(elapsed_seconds)
        hours = self.get_formatted_hours(elapsed_seconds)
        minutes = self.get_formatted_minutes(elapsed_seconds)
        seconds = self.get_formatted_seconds(elapsed_seconds)
        return f"{days}:{hours}:{minutes}:{seconds}"

    def get_seconds_since_last_update(self):
        return (current_time() - self.last_update_time).total_seconds()

    def get_time_since_last_update(self):
        return self.get_formatted_time(
            (current_time() - self.last_update_time).total_seconds())

    def get_run_time(self, formatted=True):
        if self.is_running:
            seconds_since_last_update = \
                (current_time() - self.last_update_time).total_seconds()
            return self.get_formatted_time(
                self.run_seconds + seconds_since_last_update)
        else:
            return self.get_formatted_time(self.run_seconds)

    def get_pause_time(self, formatted=True):
        if self.is_paused():
            return self.get_formatted_time(self.pause_seconds + \
                (current_time() - self.last_update_time).total_seconds())
        else:
            return self.get_formatted_time(self.pause_seconds)

    def get_state(self):
        time_since_last_update = self.get_time_since_last_update()
        if self.is_running:
            return f"Currently running for: {time_since_last_update}"
        elif self.is_paused():
            return f"Currently paused for: {time_since_last_update}"
        if self.is_stopped():
            return f"Currently stopped for: {time_since_last_update}"

    def is_paused(self):
        if self.last_update_time != self.stop_time and not self.is_running:
            return True
        else:
            return False

    def is_stopped(self):
        if self.last_update_time == self.stop_time and not self.is_running:
            return True
        else:
            return False

    def pause(self):
        if self.is_stopped() or self.is_paused():
            return None

        self.run_seconds += self.get_seconds_since_last_update()
        self.is_running = False
        self.last_update_time = current_time()
        self.save()

    def resume(self):
        if self.is_running:
            return None

        elapsed_seconds = self.get_seconds_since_last_update()
        self.pause_seconds += elapsed_seconds
        self.last_update_time = current_time()
        self.stop_time = None
        self.is_running = True
        self.save()

    def stop(self):
        if self.is_stopped():
            return None
        elif self.is_paused():
            self.pause_seconds += self.get_seconds_since_last_update()
        elif self.is_running:
            self.run_seconds += self.get_seconds_since_last_update()

        self.stop_time = current_time()
        self.last_update_time = self.stop_time

        self.is_running = False
        self.save()

    def __str__(self):
        return f"{self.activity.name} - "\
            f"Running: {self.get_run_time()}, "\
            f"Paused: {self.get_pause_time()} "\
            f"({self.get_state()})"

    def save(self, *args, **kwargs):
        if not self.start_time:
            self.start_time = timezone.now()
            self.last_update_time = self.start_time
        if not self.run_seconds:
            self.run_seconds = 0
        if not self.pause_seconds:
            self.pause_seconds = 0
        super().save(*args, **kwargs)
