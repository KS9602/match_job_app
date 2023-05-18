from .models import Employee,Employer,EmployeeJob,EmployeeLanguage
from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User

class DateInput(forms.DateInput):
    input_type = 'date'


class RegistrationEmployeeForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

class RegistrationEmployerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username','email','password1','password2')

class LoginForm(AuthenticationForm):
    class Meta:
        pass

class UpdateBaseInformationEmployeeForm(forms.ModelForm):
    
    name = forms.CharField(max_length=100,label='Imie',widget=forms.TextInput(attrs={"size": "20"}))
    last_name = forms.CharField(max_length=100,label='Nazwisko',widget=forms.TextInput(attrs={"size": "20"}))
    available_from = forms.DateField(widget=DateInput())
    available_to = forms.DateField(widget=DateInput())
    
    class Meta:
        model = Employee
        fields = ('name','last_name','available_from','available_to')



class CreateEmployeeLanguageForm(forms.ModelForm):
    class Meta:
        model = EmployeeLanguage
        fields = ('language_name','level')

class UpdateLanguageEmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeLanguage
        fields = ('language_name','level')



class CreateEmployeeJobForm(forms.ModelForm):

    job_name = forms.CharField(max_length=100,label='Stanowisko',widget=forms.TextInput(attrs={"size": "20"}))
    description = forms.CharField(max_length=200,label='Opis',widget=forms.TextInput(attrs=
                            {'cols':40,'row':3,'style':'width:300px;height:100px'}))
    work_from = forms.DateField(widget=DateInput())
    work_to = forms.DateField(widget=DateInput())

    class Meta:
        model = EmployeeJob       
        fields = ('job_name','description','work_from','work_to')



