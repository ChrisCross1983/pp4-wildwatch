# Generated by Django 4.2.17 on 2024-12-16 08:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reports", "0005_injuryreport_status"),
    ]

    operations = [
        migrations.AddField(
            model_name="injuryreport",
            name="admin_comment",
            field=models.TextField(blank=True, null=True),
        ),
    ]
