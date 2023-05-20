# Generated by Django 4.2.1 on 2023-05-18 08:40

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("match_job_app", "0006_alter_employee_available_from_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="employeejob",
            name="work_to",
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="employeejob",
            name="description",
            field=models.TextField(max_length=200, null=True),
        ),
    ]