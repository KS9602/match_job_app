from typing import Any, Dict
from django import forms
from django.core.exceptions import ValidationError
from match_job_app.constants import JOBS, LANGUAGE_CHOICES,JOB_EXPIRIENCE
from datetime import datetime
from match_job_app.validators import StringInputValidator, FileInputValidator
from match_job_app.models import (
    Employee,
    EmployeeJob,
    EmployeeLanguage,
    EmployeeJobTarget,
)

class DateInput(forms.DateInput):
    input_type = "date"


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
        fields = ("name", "last_name", "available_from", "available_to", "profile_pic")

    def clean_available_to(self) -> Dict[str, Any]:
        available_from = self.cleaned_data["available_from"]
        available_to = self.cleaned_data["available_to"]
        today = datetime.today().strftime("%Y-%m-%d")
        if available_from > available_to:
            raise ValidationError(
                "Data rozpoczęcia musi być większa od daty zakończenia"
            )
        elif datetime.strftime(available_from, "%Y-%m-%d") < today:
            raise ValidationError(
                "Data rozpoczęcia pracy nie może być wcześniejsza niż dzisiejsza"
            )
        else:
            return available_to

    def clean_name(self) -> Dict[str, Any]:
        name = self.cleaned_data["name"]
        string_validator = StringInputValidator(name)
        string_validator.only_polish_letter()
        string_validator.space_check()
        return name

    def clean_last_name(self) -> Dict[str, Any]:
        last_name = self.cleaned_data["last_name"]
        string_validator = StringInputValidator(last_name)
        string_validator.only_polish_letter()
        string_validator.space_check()
        return last_name

    def clean_profile_pic(self):
        self.profile_pic = self.cleaned_data["profile_pic"]
        file_validator = FileInputValidator(self.profile_pic)
        file_validator.allowed_size(10)
        return self.profile_pic


class CreateEmployeeLanguageForm(forms.ModelForm):
    def __init__(self, employee_user, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user = employee_user

    language_name = forms.ChoiceField(choices=LANGUAGE_CHOICES)

    class Meta:
        model = EmployeeLanguage
        fields = ("language_name", "level")

    def clean_language_name(self) -> Dict[str, Any]:
        language_name = self.cleaned_data["language_name"]
        language_name = language_name.lower()
        languages = [
            language.language_name
            for language in EmployeeLanguage.objects.filter(language_user=self.user)
        ]
        if language_name in languages:
            raise ValidationError(
                f"Język {language_name} jest już przez Ciebie wybrany"
            )
        return language_name


class EditEmployeeLanguageForm(forms.ModelForm):
    class Meta:
        model = EmployeeLanguage
        fields = ("language_name", "level")


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
    job_expirience = forms.ChoiceField(choices=JOB_EXPIRIENCE)
    work_from = forms.DateField(widget=DateInput())
    work_to = forms.DateField(widget=DateInput())

    class Meta:
        model = EmployeeJob
        fields = ("job_name", "description", "job_expirience", "work_from", "work_to")

    def clean_work_to(self) -> Dict[str, Any]:
        work_from = self.cleaned_data["work_from"]
        work_to = self.cleaned_data["work_to"]
        if work_from > work_to:
            raise ValidationError(
                "Data rozpoczęcia musi być większa od daty zakończenia"
            )
        else:
            return work_to


class AddEmployeeJobTarget(forms.ModelForm):
    def __init__(self, employee_user, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.user = employee_user

    target_name = forms.ChoiceField(choices=JOBS)

    class Meta:
        model = EmployeeJobTarget
        fields = ("target_name",)

    def clean_target_name(self) -> Dict[str, Any]:
        target_name = self.cleaned_data["target_name"]
        target_name = target_name.lower()
        targets = [
            target.target_name
            for target in EmployeeJobTarget.objects.filter(target_user=self.user)
        ]
        if target_name in targets:
            raise ValidationError(
                f"Zawód {target_name} jest już przez Ciebie poszukiwany"
            )
        return target_name
