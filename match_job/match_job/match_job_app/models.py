from django.db import models
from django.contrib.auth.models import User



class Employee(models.Model):

    user = models.OneToOneField(User,on_delete=models.CASCADE,related_name='employee')
    name = models.CharField(max_length=100,null=True)
    last_name = models.CharField(max_length=100,null=True)
    available_from = models.CharField(max_length=100,null=True)
    available_to = models.CharField (max_length=100,null=True)
    #pic 


    def __str__(self) -> str:
        return f'{self.name} {self.last_name}'


class Employer(models.Model):

    name = models.CharField(max_length=100,null=True)

    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='employer')

    def __str__(self) -> str:
        return f'{self.name}'

LANGUAGES_CHOICES = (('PL','Polish'),
                     ('ENG','English'),)

LANGUAGE_LEVEL = (('MASTER','MASTER'),
                  ('BSIC','BASIC'))

class EmployeeLanguage(models.Model):

    language_name = models.CharField(max_length=100,choices=LANGUAGES_CHOICES,default='PL')
    level = models.CharField(max_length=100,choices=LANGUAGE_LEVEL,default='MASTER')

    language_user = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='language',null=True)

    def __str__(self) -> str:
        return f'{self.language_name}'

class EmployeeJob(models.Model):

    job_name = models.CharField(max_length=100)
    description = models.TextField(max_length=200,null=True)
    work_from = models.CharField(max_length=100,null=True)
    work_to = models.CharField(max_length=100,null=True)

    job_user = models.ForeignKey(Employee,on_delete=models.CASCADE,related_name='job',null=True)

    def __str__(self) -> str:
        return f'{self.job_name}'
