from django.contrib import admin
from .models import *

admin.site.register(Employee)
admin.site.register(Employer)
admin.site.register(EmployeeJob)
admin.site.register(EmployeeLanguage)