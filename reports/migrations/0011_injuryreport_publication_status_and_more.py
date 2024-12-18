# Generated by Django 4.2.17 on 2024-12-16 17:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0010_alter_injuryreport_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="injuryreport",
            name="publication_status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Approved", "Approved"),
                    ("Rejected", "Rejected"),
                ],
                default="Pending",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="injuryreport",
            name="status",
            field=models.CharField(
                choices=[
                    ("Open", "Open"),
                    ("In Progress", "In Progress"),
                    ("Completed", "Completed"),
                ],
                default="Open",
                max_length=15,
            ),
        ),
    ]
