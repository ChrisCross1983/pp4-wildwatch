# Generated by Django 4.2.17 on 2024-12-16 17:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0011_injuryreport_publication_status_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="injuryreport",
            name="publication_status",
            field=models.CharField(
                choices=[
                    ("Pending", "Pending"),
                    ("Approved", "Approved"),
                    ("Rejected", "Rejected"),
                ],
                default="Open",
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
                default="Pending",
                max_length=15,
            ),
        ),
    ]
