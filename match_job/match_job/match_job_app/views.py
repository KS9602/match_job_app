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


@method_decorator(checking_role("employee"), name="dispatch")
class EmployeeProfile(LoginRequiredMixin, DetailView):
    login_url = "login"
    template_name = "employee_profile.html"
    model = Employee

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        employee_user = Employee.objects.get(pk=self.kwargs["pk"])
        jobs = EmployeeJob.objects.filter(job_user=employee_user)
        languages = EmployeeLanguage.objects.filter(language_user=employee_user)
        targets = EmployeeJobTarget.objects.filter(target_user=employee_user)
        if len(targets) > 0:
            targets = targets.last().target_name
            targets = targets.split(",")

        (
            context["employee_user"],
            context["jobs"],
            context["languages"],
            context["targets"],
        ) = (employee_user, jobs, languages, targets)
        return context


@method_decorator(checking_role("employee"), name="dispatch")
class EditBaseInformationEmployeeView(LoginRequiredMixin, UpdateView):
    login_url = "login"
    template_name = "update_information_employee.html"
    pk_url_kwarg = "pk"
    model = Employee
    form_class = UpdateBaseInformationEmployeeForm

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employee_profile", kwargs={"pk": pk})
        return url

    def form_valid(self, form: BaseModelForm) -> HttpResponse:
        return super().form_valid(form)


@method_decorator(checking_role("employee"), name="dispatch")
class AddLanguageView(LoginRequiredMixin, CreateView): 
    login_url = "login"
    template_name = "add_language.html"
    model = EmployeeLanguage
    form_class = CreateEmployeeLanguageForm

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employee_profile", kwargs={"pk": pk})
        return url

    def get_form_kwargs(self) -> Dict[str, Any]:
        kargs = super().get_form_kwargs()
        kargs["employee_user"] = self.request.user.employee
        return kargs

    def form_valid(self, form: CreateEmployeeLanguageForm) -> HttpResponse:
        form = self.get_form(CreateEmployeeLanguageForm)
        user = Employee.objects.get(user=self.request.user)
        form.instance.language_user = user
        return super().form_valid(form)


@method_decorator(checking_role("employee"), name="dispatch")
class EditLanguageView(LoginRequiredMixin, UpdateView): 
    login_url = "login"
    template_name = "update_language.html"
    pk_url_kwarg = "pk_lang"
    model = EmployeeLanguage
    form_class = CreateEmployeeLanguageForm

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employee_profile", kwargs={"pk": pk})
        return url

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> EmployeeLanguage:
        language = EmployeeLanguage.objects.get(id=self.kwargs["pk_lang"])
        return language

    def get_form_kwargs(self) -> Dict[str, Any]:
        kwargs = super().get_form_kwargs()
        kwargs["employee_user"] = self.request.user.employee
        return kwargs


@method_decorator(checking_role("employee"), name="dispatch")
class DeleteLanguageView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    context_object_name = "language"
    pk_url_kwarg = "pk_lang"
    model = EmployeeLanguage

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


@method_decorator(checking_role("employee"), name="dispatch")
class AddJobView(LoginRequiredMixin, CreateView):
    template_name = "add_job_history.html"  
    login_url = "login"
    model = EmployeeJob
    form_class = CreateEmployeeJobForm

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employee_profile", kwargs={"pk": pk})
        return url

    def form_valid(self, form: CreateEmployeeJobForm) -> HttpResponse:
        form = CreateEmployeeJobForm(self.request.POST)
        user = Employee.objects.get(user=self.request.user)
        form.instance.job_user = user
        return super().form_valid(form)


@method_decorator(checking_role("employee"), name="dispatch")
class EditJobView(LoginRequiredMixin, UpdateView):
    login_url = "login"  
    template_name = "update_job.html"
    pk_url_kwarg = "pk_job"
    model = EmployeeJob
    form_class = CreateEmployeeJobForm

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employee_profile", kwargs={"pk": pk})
        return url

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> EmployeeLanguage:
        job = EmployeeJob.objects.get(id=self.kwargs["pk_job"])
        return job


@method_decorator(checking_role("employee"), name="dispatch")
class DeleteJobView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    context_object_name = "job"
    pk_url_kwarg = "pk_job"
    model = EmployeeJob

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


@method_decorator(checking_role("employee"), name="dispatch")
class AddEmployeeTargetJobView(LoginRequiredMixin, CreateView):
    login_url = "login"
    template_name = "add_job_target.html"
    model = EmployeeJobTarget
    form_class = AddEmployeeJobTarget

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employee_profile", kwargs={"pk": pk})
        return url

    def form_valid(self, form: AddEmployeeJobTarget) -> HttpResponse:
        form = AddEmployeeJobTarget(self.request.POST)
        user = Employee.objects.get(user=self.request.user)
        form.instance.target_user = user

        return super().form_valid(form)


@method_decorator(checking_role("employer"), name="dispatch")
class EmployerProfileView(LoginRequiredMixin, DetailView):
    login_url = "login"    
    template_name = "employer_profile.html"
    model = Employer

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = Employer.objects.get(id=self.kwargs["pk"])
        context["employer"] = Employer.objects.get(id=self.kwargs["pk"])
        context["job_posts"] = JobPost.objects.filter(employer=user)
        return context


@method_decorator(checking_role("employer"), name="dispatch")
class EditBaseInformationEmployerView(LoginRequiredMixin, UpdateView):
    login_url = "login"
    template_name = "update_information_employer.html"
    pk_url_kwarg = "pk"
    model = Employer
    form_class = UpdateBaseInformationEmployerForm

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employer_profile", kwargs={"pk": pk})
        return url


@method_decorator(checking_role("employer"), name="dispatch")
class AddJEmployerobPostView(LoginRequiredMixin, CreateView):
    login_url = "login"
    template_name = "add_job_post.html"
    model = JobPost
    form_class = CreateJobPostForm

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employer_profile", kwargs={"pk": pk})
        return url

    def form_valid(self, form: CreateJobPostForm) -> HttpResponse:
        form = CreateJobPostForm(self.request.POST)
        user = Employer.objects.get(user=self.request.user)
        form.instance.employer = user
        return super().form_valid(form)


@method_decorator(checking_role("employer"), name="dispatch")
class EditEmployerJobPostView(LoginRequiredMixin, UpdateView):
    login_url = "login"
    template_name = "edit_job_post.html"
    pk_url_kwarg = "pk_post"
    model = JobPost
    form_class = CreateJobPostForm

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employer_profile", kwargs={"pk": pk})
        return url

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> JobPost:
        job_post = JobPost.objects.get(id=self.kwargs["pk_post"])
        return job_post
    

class ShowEmployeesView(LoginRequiredMixin,ListView):
    login_url = "login"
    template_name = "show_employee.html"
    context_object_name = 'employees'
    paginate_by = 6
    queryset = Employee.objects.all()


class PublicEmployeeProfileView(LoginRequiredMixin, DetailView):
    login_url = "login"
    template_name = 'public_employee_profile.html'
    context_object_name = 'employee'
    model = Employee

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        employee = Employee.objects.get(pk=self.kwargs["pk"])
        jobs = EmployeeJob.objects.filter(job_user=employee)
        languages = EmployeeLanguage.objects.filter(language_user=employee)
        targets = EmployeeJobTarget.objects.filter(target_user=employee)

        if len(targets) > 0:
            targets = targets.last().target_name
            targets = targets.split(",")

        (
            context["employee"],
            context["jobs"],
            context["languages"],
            context["targets"],
        ) = (employee, jobs, languages, targets)
        return context
