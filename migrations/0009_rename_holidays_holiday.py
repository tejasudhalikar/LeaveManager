# Generated by Django 4.2.7 on 2023-11-17 10:57

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("LeaveManager", "0008_holidays_alter_leaveaccruement_unit_and_more"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Holidays",
            new_name="Holiday",
        ),
    ]
