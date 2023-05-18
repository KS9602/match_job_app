# Generated by Django 4.2.1 on 2023-05-17 09:36

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("match_job_app", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employee",
            name="user",
            field=models.OneToOneField(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="employee",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name="employer",
            name="name",
            field=models.CharField(max_length=100, null=True),
        ),
    ]
