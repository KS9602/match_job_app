from django import forms
from ..validators import FileInputValidator
from ..models import (
    Employer,
    JobPost,
)

class UpdateBaseInformationEmployerForm(forms.ModelForm):
    company_name = forms.CharField(
        max_length=100, label="Nazwa", widget=forms.TextInput(attrs={"size": "20"})
    )
    company_address = forms.CharField(
        max_length=200, label="Adres", widget=forms.TextInput(attrs={"size": "20"})
    )
    company_description = forms.CharField(
        max_length=600, label="Opis", widget=forms.TextInput(attrs={"size": "20"})
    )
    company_pic = forms.FileField(label="Logo")

    class Meta:
        model = Employer
        fields = (
            "company_name",
            "company_address",
            "company_description",
            "company_pic",
        )

    def clean_company_pic(self):
        self.company_pic = self.cleaned_data["company_pic"]
        file_validator = FileInputValidator(self.company_pic)
        file_validator.allowed_size(10)
        return self.company_pic


class CreateJobPostForm(forms.ModelForm):
    title = forms.CharField(
        max_length=100,
        label="Tytuł ogłoszenia",
        widget=forms.TextInput(attrs={"size": "20"}),
    )
    description = forms.CharField(
        max_length=600,
        label="Opis",
        widget=forms.TextInput(attrs={"style": "width:300px;height:100px"}),
    )
    requirements = forms.CharField(
        max_length=600,
        label="Wymagania",
        widget=forms.TextInput(attrs={"style": "width:300px;height:100px"}),
    )

    class Meta:
        model = JobPost
        fields = ("title", "description",)


