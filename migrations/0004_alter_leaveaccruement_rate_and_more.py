# Generated by Django 4.2.7 on 2023-11-17 06:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        (
            "LeaveManager",
            "0003_leaveaccruement_remove_leavetype_carry_forward_and_more",
        ),
    ]

    operations = [
        migrations.AlterField(
            model_name="leaveaccruement",
            name="rate",
            field=models.FloatField(),
        ),
        migrations.AlterField(
            model_name="leavetype",
            name="encash_offset_days",
            field=models.IntegerField(blank=True, default=None, null=True),
        ),
        migrations.AlterField(
            model_name="leavetype",
            name="is_encashable",
            field=models.BooleanField(default=False),
        ),
    ]
