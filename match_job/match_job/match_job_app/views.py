from typing import Any, Optional, Type, Union
from django import http
from django.db import models
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.views.generic import (
    FormView,
    CreateView,
    TemplateView,
    DeleteView,
    View,
    UpdateView,
    DetailView,
    ListView,
)
from .forms import *
from .models import *
from django.contrib.auth import logout, login, authenticate
from django.contrib import messages
from typing import Any, Dict
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.mixins import UserPassesTestMixin
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.decorators import method_decorator
from .decorators import checking_role


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

@method_decorator(checking_role('employee'), name="dispatch")
class EmployeeProfile(LoginRequiredMixin, DetailView):
    template_name = "employee_profile.html"
    model = Employee
    login_url = "login"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        employee_user = Employee.objects.get(pk=self.kwargs["pk"])
        jobs = EmployeeJob.objects.filter(job_user=employee_user)
        languages = EmployeeLanguage.objects.filter(language_user=employee_user)
        targets = EmployeeJobTarget.objects.filter(target_user=employee_user)
        if len(targets) > 0:
            targets = targets.last().target_name
            targets = targets.split(',')

        context["employee_user"], context["jobs"], context["languages"],context['targets'] = (
            employee_user,
            jobs,
            languages,
            targets
        )
        return context


class EmployerProfile(LoginRequiredMixin, DetailView):
    template_name = "employer_profile.html"
    model = Employer
    login_url = "login"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        context["employer"] = Employer.objects.get(id=self.kwargs["pk"])
        return context


@method_decorator(checking_role('employee'), name="dispatch")
class EditBaseInformationEmployeeView(LoginRequiredMixin, UpdateView):
    template_name = "update_information_employee.html"
    login_url = "login"
    model = Employee
    form_class = UpdateBaseInformationEmployeeForm
    pk_url_kwarg = "pk"

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employee_profile", kwargs={"pk": pk})
        return url

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        print(self.request.POST)
        return super().form_valid(form)
    

@method_decorator(checking_role('employee'), name="dispatch")
class AddLanguageView(LoginRequiredMixin, CreateView):
    login_url = "login"
    model = EmployeeLanguage
    form_class = CreateEmployeeLanguageForm
    template_name = "add_language.html"

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employee_profile", kwargs={"pk": pk})
        return url
    
    def get_form_kwargs(self) -> Dict[str, Any]:
        kargs = super().get_form_kwargs()
        kargs['employee_user'] = self.request.user.employee
        return kargs

    def form_valid(self, form: CreateEmployeeLanguageForm) -> HttpResponse:
        form = self.get_form(CreateEmployeeLanguageForm)
        user = Employee.objects.get(user=self.request.user)
        form.instance.language_user = user
        return super().form_valid(form)

@method_decorator(checking_role('employee'), name="dispatch")
class EditLanguageView(LoginRequiredMixin, UpdateView):
    template_name = "update_language.html"
    login_url = "login"
    model = EmployeeLanguage
    form_class = UpdateLanguageEmployeeForm
    pk_url_kwarg = "pk_lang"

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employee_profile", kwargs={"pk": pk})
        return url
    
    def get_object(self, queryset: QuerySet[Any] | None = ...) -> EmployeeLanguage:
        language = EmployeeLanguage.objects.get(id=self.kwargs["pk_lang"])
        return language


@method_decorator(checking_role('employee'), name="dispatch")
class DeleteLanguageView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    model = EmployeeLanguage
    context_object_name = "language"
    pk_url_kwarg = "pk_lang"

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employee_profile", kwargs={"pk": pk})
        return url

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> EmployeeLanguage:
        language = EmployeeLanguage.objects.get(id=self.kwargs["pk_lang"])
        return language

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


@method_decorator(checking_role('employee'), name="dispatch")
class AddJobView(LoginRequiredMixin, CreateView):
    login_url = "login"
    model = EmployeeJob
    form_class = CreateEmployeeJobForm
    template_name = "add_job_history.html"

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employee_profile", kwargs={"pk": pk})
        return url

    def form_valid(self, form: CreateEmployeeJobForm) -> HttpResponse:
        form = CreateEmployeeJobForm(self.request.POST)
        user = Employee.objects.get(user=self.request.user)
        form.instance.job_user = user
        return super().form_valid(form)


@method_decorator(checking_role('employee'), name="dispatch")
class EditJobView(LoginRequiredMixin, UpdateView):
    template_name = "update_job.html"
    login_url = "login"
    model = EmployeeJob
    form_class = UpdateJobEmployeeForm
    pk_url_kwarg = "pk_job"

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employee_profile", kwargs={"pk": pk})
        return url

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> EmployeeLanguage:
        job = EmployeeJob.objects.get(id=self.kwargs["pk_job"])
        return job


@method_decorator(checking_role('employee'), name="dispatch")
class DeleteJobView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    model = EmployeeJob
    context_object_name = "job"
    pk_url_kwarg = "pk_job"

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employee_profile", kwargs={"pk": pk})
        return url

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> EmployeeJob:
        language = EmployeeJob.objects.get(id=self.kwargs["pk_job"])
        return language

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)


@method_decorator(checking_role('employee'), name="dispatch")
class EditBaseInformationEmployerView(LoginRequiredMixin, TemplateView):
    template_name = ""
    login_url = "login"

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        return super().get_context_data(**kwargs)


@method_decorator(checking_role('employee'), name="dispatch")
class AddEmployeeTargetJob(LoginRequiredMixin, CreateView):
    login_url = "login"
    model = EmployeeJobTarget
    form_class = AddEmployeeJobTarget
    template_name = "add_job_target.html"

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employee_profile", kwargs={"pk": pk})
        return url

    def form_valid(self, form: AddEmployeeJobTarget) -> HttpResponse:
        form = AddEmployeeJobTarget(self.request.POST)
        user = Employee.objects.get(user=self.request.user)
        form.instance.target_user = user

        return super().form_valid(form)