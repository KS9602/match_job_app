from django.db import models
from django.contrib.auth.models import User
from .constants import LANGUAGE_CHOICES, LANGUAGE_LEVEL_CHOICES


def user_directory_path(instance, filename):
    user = instance.user.id
    file = filename
    return f"user_{user}/{file}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")
    name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=100, null=True)
    available_from = models.CharField(max_length=50, null=True)
    available_to = models.CharField(max_length=50, null=True)
    profile_pic = models.ImageField(
        upload_to=user_directory_path, null=True, blank=True
    )
    created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self) -> str:
        return f"{self.name} {self.last_name}"


class EmployeeLanguage(models.Model):
    language_name = models.CharField(
        max_length=50, choices=LANGUAGE_CHOICES, default="Polski"
    )
    level = models.CharField(
        max_length=50, choices=LANGUAGE_LEVEL_CHOICES, default="MASTER"
    )
    language_user = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="language", null=True
    )
    created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self) -> str:
        return f"{self.language_name}"


class EmployeeJob(models.Model):
    job_name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, null=True)
    work_from = models.CharField(max_length=50, null=True)
    work_to = models.CharField(max_length=50, null=True)
    job_user = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="job", null=True
    )
    created = models.DateTimeField(auto_now_add=True,null=True)

    def __str__(self) -> str:
        return f"{self.job_name}"


class EmployeeJobTarget(models.Model):
    target_name = models.CharField(max_length=50)
    target_user = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="target", null=True
    )
    created = models.DateTimeField(auto_now_add=True,null=True)


class Employer(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employer")
    company_name = models.CharField(max_length=100,null=True)
    company_address = models.CharField(max_length=200,null=True)
    company_description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    #company_logo = models.ImageField(upload_to='logos/', blank=True, null=True)
    
    def __str__(self) -> str:
        return f"{self.company_name}"
    

class JobPost(models.Model):
    title = models.CharField(max_length=100,null=True)
    description = models.TextField(null=True)
    requirements = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True,null=True)
    employer = models.ForeignKey('Employer', on_delete=models.CASCADE)

    def __str__(self):
        return self.title