from typing import Any
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import (
    CreateView,
    DeleteView,
    UpdateView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.decorators import method_decorator
from match_job_app.decorators.checking_role import checking_role
from .employee_forms import (
    CreateEmployeeJobForm,
)
from match_job_app.models import (
    Employee,
    EmployeeJob,
    EmployeeLanguage,
)


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
