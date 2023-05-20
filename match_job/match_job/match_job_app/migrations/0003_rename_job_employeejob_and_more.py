# Generated by Django 4.2.1 on 2023-05-17 13:57

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("match_job_app", "0002_alter_employee_user_alter_employer_name"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Job",
            new_name="EmployeeJob",
        ),
        migrations.RenameModel(
            old_name="Language",
            new_name="EmployeeLanguage",
        ),
    ]