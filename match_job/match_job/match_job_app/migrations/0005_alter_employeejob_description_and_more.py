# Generated by Django 4.2.1 on 2023-05-17 19:26

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("match_job_app", "0004_remove_employeejob_experience_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="employeejob",
            name="description",
            field=models.TextField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name="employeejob",
            name="work_from",
            field=models.DateField(max_length=100, null=True),
        ),
    ]
