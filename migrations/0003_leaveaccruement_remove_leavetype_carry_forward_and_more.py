# Generated by Django 4.2.7 on 2023-11-17 06:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("LeaveManager", "0002_leavetype_alter_employee_contact_number_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="LeaveAccruement",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "dtm_created",
                    models.DateTimeField(auto_now_add=True, verbose_name="DTM Created"),
                ),
                (
                    "dtm_updated",
                    models.DateTimeField(auto_now=True, verbose_name="DTM Updated"),
                ),
                ("rate", models.IntegerField()),
                ("unit", models.CharField(max_length=20)),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.RemoveField(
            model_name="leavetype",
            name="carry_forward",
        ),
        migrations.AddField(
            model_name="leavetype",
            name="carry_forward_days",
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name="leavetype",
            name="accruement",
            field=models.ForeignKey(
                blank=True,
                default=None,
                null=True,
                on_delete=django.db.models.deletion.DO_NOTHING,
                to="LeaveManager.leaveaccruement",
            ),
        ),
    ]
