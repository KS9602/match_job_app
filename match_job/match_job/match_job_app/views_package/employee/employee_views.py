from typing import Any, Dict
from django.shortcuts import redirect
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponse
from django.views.generic import (
    UpdateView,
    DetailView,
    ListView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.decorators import method_decorator
from match_job_app.decorators.checking_role import checking_role
from .employee_forms import (
    EmployeeJobTarget,
    UpdateBaseInformationEmployeeForm,
)
from match_job_app.models import Employee, EmployeeJob, EmployeeLanguage, EmployeeJobTarget


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


class ShowEmployeesView(LoginRequiredMixin, ListView):
    login_url = "login"
    template_name = "show_employees.html"
    context_object_name = "employees"
    paginate_by = 6
    queryset = Employee.objects.all()
    pk_url_kwarg = "target_filter"

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()
        try:
            target_filter = self.kwargs["target_filter"]
        except:
            return queryset
        queryset = Employee.objects.filter(target__target_name__icontains=target_filter)
        return queryset

    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        target_filter = self.request.POST.get("target_filter")
        target_filter = target_filter.lower()
        return redirect("show_employees_filtered", target_filter)


class PublicEmployeeProfileView(LoginRequiredMixin, DetailView):
    login_url = "login"
    template_name = "public_employee_profile.html"
    context_object_name = "employee"
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
