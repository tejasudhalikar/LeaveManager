# Generated by Django 4.2.7 on 2023-11-17 12:13

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("LeaveManager", "0009_rename_holidays_holiday"),
    ]

    operations = [
        migrations.AddField(
            model_name="leave",
            name="date",
            field=models.DateField(default=datetime.date(2023, 11, 17)),
            preserve_default=False,
        ),
    ]