from django.contrib.auth.models import AbstractUser
from django.db import models
from timezone_field import TimeZoneField

class TimerUser(AbstractUser):
    timezone = TimeZoneField(default='Canada/Mountain')
