# Generated by Django 3.1.3 on 2020-11-17 21:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0002_auto_20201117_2059'),
    ]

    operations = [
        migrations.RenameField(
            model_name='timer',
            old_name='pause_timestamp',
            new_name='pause_time',
        ),
        migrations.RenameField(
            model_name='timer',
            old_name='start_timestamp',
            new_name='start_time',
        ),
        migrations.RenameField(
            model_name='timer',
            old_name='stop_timestamp',
            new_name='stop_time',
        ),
    ]
