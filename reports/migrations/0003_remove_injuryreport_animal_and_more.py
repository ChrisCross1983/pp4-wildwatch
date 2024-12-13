# Generated by Django 4.2.17 on 2024-12-13 13:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("reports", "0002_alter_injuryreport_reported_by"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="injuryreport",
            name="animal",
        ),
        migrations.RemoveField(
            model_name="injuryreport",
            name="comments",
        ),
        migrations.RemoveField(
            model_name="injuryreport",
            name="report_status",
        ),
        migrations.AlterField(
            model_name="injuryreport",
            name="gender",
            field=models.CharField(
                choices=[
                    ("Male", "Male"),
                    ("Female", "Female"),
                    ("Unknown", "Unknown"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="injuryreport",
            name="injury_condition",
            field=models.CharField(
                choices=[
                    ("Slightly Injured", "Slightly Injured"),
                    ("Seriously Injured", "Seriously Injured"),
                    ("Not Injured", "Not Injured"),
                ],
                max_length=50,
            ),
        ),
        migrations.AlterField(
            model_name="injuryreport",
            name="location",
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name="injuryreport",
            name="reported_by",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="injuryreport",
            name="species",
            field=models.CharField(
                choices=[("Cat", "Cat"), ("Dog", "Dog")], max_length=50
            ),
        ),
    ]
