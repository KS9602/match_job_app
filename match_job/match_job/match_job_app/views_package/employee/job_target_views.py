from typing import Any, Dict
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import (
    CreateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.decorators import method_decorator
from match_job_app.decorators.checking_role import checking_role
from .employee_forms import EmployeeJobTarget, AddEmployeeJobTarget
from match_job_app.models import Employee, EmployeeJobTarget


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

    def get_form_kwargs(self) -> Dict[str, Any]:
        kargs = super().get_form_kwargs()
        kargs["employee_user"] = self.request.user.employee
        return kargs

    def form_valid(self, form: AddEmployeeJobTarget) -> HttpResponse:
        form = self.get_form(AddEmployeeJobTarget)
        user = Employee.objects.get(user=self.request.user)
        form.instance.target_user = user
        return super().form_valid(form)


@method_decorator(checking_role("employee"), name="dispatch")
class DeleteEmployeeTargetView(LoginRequiredMixin, DeleteView):
    login_url = "login"
    context_object_name = "job_target"
    pk_url_kwarg = "pk_job_target"
    model = EmployeeJobTarget

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employee_profile", kwargs={"pk": pk})
        return url

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> EmployeeJobTarget:
        language = EmployeeJobTarget.objects.get(id=self.kwargs["pk_job_target"])
        return language

    def delete(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.delete()
        return HttpResponseRedirect(success_url)
