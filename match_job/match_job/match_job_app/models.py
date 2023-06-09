from django.db import models
from django.contrib.auth.models import User
from django.core.validators import FileExtensionValidator
from .constants import LANGUAGE_LEVEL_CHOICES, JOB_EXPIRIENCE


def employee_directory_path(instance, filename):
    user = instance.user
    file = filename
    return f"employee_{user}/{file}"


def employer_directory_path(instance, filename):
    user = instance.user
    file = filename
    return f"employer_{user}/{file}"


class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="employee")
    name = models.CharField(max_length=50, null=True)
    last_name = models.CharField(max_length=100, null=True)
    available_from = models.CharField(max_length=50, null=True)
    available_to = models.CharField(max_length=50, null=True)
    profile_pic = models.ImageField(
        default="default.jpeg",
        upload_to=employee_directory_path,
        null=True,
        blank=True,
        validators=[FileExtensionValidator(["jpg", "png", "jpeg"])],
    )
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f"{self.name} {self.last_name}"


class EmployeeLanguage(models.Model):
    language_name = models.CharField(max_length=50, default="Polski")
    level = models.CharField(
        max_length=50, choices=LANGUAGE_LEVEL_CHOICES, default="MASTER"
    )
    language_user = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="language", null=True
    )
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f"{self.language_name}"


class EmployeeJob(models.Model):
    job_name = models.CharField(max_length=50)
    description = models.TextField(max_length=200, null=True)
    job_expirience = models.IntegerField( choices=JOB_EXPIRIENCE, default=1, null=True)
    work_from = models.CharField(max_length=50, null=True)
    work_to = models.CharField(max_length=50, null=True)
    job_user = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="job", null=True
    )
    created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self) -> str:
        return f"{self.job_name}"


class EmployeeJobTarget(models.Model):
    target_name = models.CharField(max_length=300)
    target_user = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="target", null=True
    )
    created = models.DateTimeField(auto_now_add=True, null=True)


class Employer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="employer")
    company_name = models.CharField(max_length=100, null=True)
    company_address = models.CharField(max_length=200, null=True)
    company_description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    company_pic = models.ImageField(
        default="default.jpeg",
        upload_to=employer_directory_path,
        blank=True,
        null=True,
        validators=[FileExtensionValidator(["jpg", "png", "jpeg"])],
    )

    def __str__(self) -> str:
        return f"{self.company_name}"


class JobPost(models.Model):
    title = models.CharField(max_length=100, null=True)
    description = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True, null=True)
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class JobPostRequirementMustHave(models.Model):
    requirement = models.CharField(max_length=100, null=True)
    job_post = models.ForeignKey(
        JobPost, on_delete=models.CASCADE, related_name="job_post_requirement_must_have"
    )


class JobPostRequirementOptional(models.Model):
    requirement = models.CharField(max_length=100, null=True)
    job_post = models.ForeignKey(
        JobPost,
        on_delete=models.CASCADE,
        related_name="job_post_requirement_nice_to_have",
    )


class JobPostFeature(models.Model):
    feature = models.CharField(max_length=100, null=True)
    job_post = models.ForeignKey(
        JobPost, on_delete=models.CASCADE, related_name="job_post_feature"
    )
