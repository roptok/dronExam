# Generated by Django 5.1.5 on 2025-03-02 09:00

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cinema', '0002_alter_cinemauser_age_alter_cinemauser_phone'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='session',
            name='date',
        ),
        migrations.AddField(
            model_name='session',
            name='startDate',
            field=models.DateTimeField(db_column='session_dt', default=datetime.datetime(2025, 3, 2, 16, 0, 8, 508075)),
            preserve_default=False,
        ),
    ]
