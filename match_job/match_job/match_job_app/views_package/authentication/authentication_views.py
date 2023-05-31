from django.http import HttpResponse
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib import messages
from django.views.generic import (
TemplateView,
CreateView,
FormView,
View,
)
from match_job_app.forms.authentication_forms import (
RegistrationEmployeeForm,
RegistrationEmployerForm,
LoginForm,
)
from django.contrib.auth import (
    logout,
    login,
    authenticate
)
from match_job_app.models import (
Employee,
Employer
)

class ChoiceRoleView(TemplateView):
    template_name = "choice_role.html"
class RegistrationEmployeeView(CreateView):
    template_name = "registration_employee.html"
    success_url = "login"
    form_class = RegistrationEmployeeForm

    def form_valid(self, form: RegistrationEmployeeForm) -> HttpResponse:
        user = form.save()
        group = Group.objects.get(name="employee")
        user.groups.add(group)
        new_employee = Employee(user=user)
        new_employee.save()
        messages.info(self.request, f"Zarejestrowano użytkownika {user.username}")
        return super().form_valid(form)


class RegistrationEmployerView(CreateView):
    template_name = "registration_employee.html"
    success_url = "login"
    form_class = RegistrationEmployeeForm

    def form_valid(self, form: RegistrationEmployerForm) -> HttpResponse:
        user = form.save()
        group = Group.objects.get(name="employer")
        user.groups.add(group)
        new_employee = Employer(user=user)
        new_employee.save()
        messages.info(self.request, f"Zarejestrowano użytkownika {user.username}")
        return super().form_valid(form)


class LoginView(FormView):
    template_name = "login.html"
    form_class = LoginForm

    def form_valid(self, form: LoginForm) -> HttpResponse:
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user = authenticate(self.request, username=username, password=password)
        if user is not None:
            login(self.request, user=user)
            return redirect("home")
        else:
            return redirect("login")


class LogoutView(View):
    def get(self, *args, **kwargs) -> HttpResponse:
        logout(self.request)
        return redirect("home")