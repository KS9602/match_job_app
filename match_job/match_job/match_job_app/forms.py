from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

from .employer.employer_froms import *
from .employee.employee_forms import *


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


class ChoiceTypeOfEmployee(
    forms.Form
):  # do zmiany jak zostanie poprawiny front home (formularz do pracy na wakcje)
    choice_field = forms.ChoiceField(
        choices=((1, "xxx"), (2, "zzz")),
        widget=forms.ChoiceField,
    )
