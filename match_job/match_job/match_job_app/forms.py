from typing import Any, Dict
from .models import Employee, Employer, EmployeeJob, EmployeeLanguage,EmployeeJobTarget
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .constants import JOBS
from datetime import datetime
from string import ascii_letters

class DateInput(forms.DateInput):
    input_type = "date"


class RegistrationEmployeeForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class RegistrationEmployerForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class LoginForm(AuthenticationForm):
    class Meta:
        pass


class UpdateBaseInformationEmployeeForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100, label="Imie", widget=forms.TextInput(attrs={"size": "20"})
    )
    last_name = forms.CharField(
        max_length=100, label="Nazwisko", widget=forms.TextInput(attrs={"size": "20"})
    )
    available_from = forms.DateField(widget=DateInput())
    available_to = forms.DateField(widget=DateInput())
    profile_pic = forms.FileField()

    class Meta:
        model = Employee
        fields = ("name", "last_name", "available_from", "available_to",'profile_pic')


    def clean_available_to(self) -> Dict[str, Any]:
        available_from = self.cleaned_data['available_from']
        available_to = self.cleaned_data['available_to']
        today = datetime.today().strftime("%Y-%m-%d")
        if available_from > available_to:
            raise ValidationError('Data rozpoczęcia musi być większa od daty zakończenia')
        elif datetime.strftime(available_from,"%Y-%m-%d"
        ) < today:
            raise ValidationError('Data rozpoczęcia pracy nie może być wcześniejsza niż dzisiejsza')
        else:
            return available_to
        

    def clean_name(self) -> Dict[str, Any]:
        name = self.cleaned_data['name']

        for letter in name:
            if letter not in ascii_letters or letter == ' ':
                raise ValidationError('Niedozwolone znaki')
        return name

    def clean_last_name(self) -> Dict[str, Any]:
        name = self.cleaned_data['last_name']

        for letter in name:
            if letter not in ascii_letters or letter == ' ':
                raise ValidationError('Niedozwolone znaki')
        return name
        """ZROBIC FUNKCJE KTORA BEDZIE SPRAWDZALA CZY ZNAKI TO LITERY + ĄĆ ITD. czy nie ma spacji i co tam sie wymysli
        potem pododawac ta funkcje do cleanow typu imie,nazwisko,nazwa firmy itd"""


    
class CreateEmployeeLanguageForm(forms.ModelForm):

    def __init__(self,*args,**kwargs) -> None:
        self.user = kwargs.pop('employee_user')
        super().__init__(*args,**kwargs)

    class Meta:
        model = EmployeeLanguage
        fields = ("language_name", "level")

    def clean_language_name(self):
        language_name = self.cleaned_data['language_name']
        user_languages = EmployeeLanguage.objects.filter(language_user=self.user)
        languages_list = [language.language_name for language in user_languages]
        if language_name in languages_list:
            raise ValidationError('Ten język jest już wybrany')
        return language_name


class UpdateLanguageEmployeeForm(forms.ModelForm):
    class Meta:
        model = EmployeeLanguage
        fields = ("language_name", "level",)


class CreateEmployeeJobForm(forms.ModelForm):
    job_name = forms.CharField(
        max_length=100, label="Stanowisko", widget=forms.TextInput(attrs={"size": "20"})
    )
    description = forms.CharField(
        max_length=200,
        label="Opis",
        widget=forms.TextInput(
            attrs={"cols": 40, "row": 3, "style": "width:300px;height:100px"}
        ),
    )
    work_from = forms.DateField(widget=DateInput())
    work_to = forms.DateField(widget=DateInput())

    class Meta:
        model = EmployeeJob
        fields = ("job_name", "description", "work_from", "work_to")

    def clean_work_to(self)  -> Dict[str, Any]:
        work_from = self.cleaned_data['work_from']
        work_to = self.cleaned_data['work_to']
        if work_from > work_to:
            raise ValidationError('Data rozpoczęcia musi być większa od daty zakończenia')
        else:
            return work_to


class UpdateJobEmployeeForm(forms.ModelForm):
    job_name = forms.CharField(
        max_length=100, label="Stanowisko", widget=forms.TextInput(attrs={"size": "20"})
    )
    description = forms.CharField(
        max_length=200,
        label="Opis",
        widget=forms.TextInput(
            attrs={"cols": 40, "row": 3, "style": "width:300px;height:100px"}
        ),
    )
    work_from = forms.DateField(widget=DateInput())
    work_to = forms.DateField(widget=DateInput())

    class Meta:
        model = EmployeeJob
        fields = ("job_name", "description", "work_from", "work_to")

    def clean_work_to(self) -> Dict[str, Any]:
        work_from = self.cleaned_data['work_from']
        work_to = self.cleaned_data['work_to']
        if work_from > work_to:
            raise ValidationError('Data rozpoczęcia musi być większa od daty zakończenia')
        else:
            return work_to


class AddEmployeeJobTarget(forms.ModelForm):

    target_name = forms.MultipleChoiceField(choices=JOBS)
    class Meta:
        model = EmployeeJobTarget
        fields = ('target_name',)

    def clean_target_name(self) -> Dict[str, Any]:
        target_name = self.cleaned_data['target_name']
        target_name = ','.join(target_name)
        return target_name

