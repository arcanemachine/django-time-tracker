# Generated by Django 3.1.3 on 2020-11-17 20:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_squashed_0007_auto_20201117_0917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='timer',
            name='start_timestamp',
            field=models.DateTimeField(),
        ),
    ]
