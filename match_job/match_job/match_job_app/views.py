from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponse
from django.shortcuts import redirect,get_object_or_404
from django.views.generic import (
    FormView,
    CreateView,
    TemplateView,
    View,
)
from .forms import *
from .models import *
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from django.contrib.auth.models import Group


from .employer_views import *
from .employee_views import *

def init_app(request):
    if Group.objects.all().count() < 2:
        employee_group = Group(name="employee")
        employer_group = Group(name="employer")
        employee_group.save()
        employer_group.save()
    return redirect("home")


class HomeView(TemplateView):
    template_name = "home.html"
    context_object_name = "user_role"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        if self.request.user.groups.first() != None:
            if self.request.user.groups.first().name == "employer":
                context["user_role"] = "employer"
                user_role_model = get_object_or_404(Employer, user=self.request.user)
                context["user_role_model"] = user_role_model
                return context
            if self.request.user.groups.first().name == "employee":
                context["user_role"] = "employee"
                user_role_model = get_object_or_404(Employee, user=self.request.user)
                context["user_role_model"] = user_role_model
                print
                return context
        return context

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return super().get(request, *args, **kwargs)

    def post(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        if self.request.POST.get("job_choice") == "employee":
            return redirect("home")  # zmienic linki
        else:
            return redirect("home")


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


