from typing import Any, Dict
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
from ..decorators import checking_role
from .employee_forms import (
    CreateEmployeeLanguageForm,
    EditEmployeeLanguageForm,
)
from ..models import (
    Employee,
    EmployeeLanguage,
)


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
    form_class = EditEmployeeLanguageForm

    def get_success_url(self) -> str:
        pk = self.kwargs["pk"]
        url = reverse("employee_profile", kwargs={"pk": pk})
        return url

    def get_object(self, queryset: QuerySet[Any] | None = ...) -> EmployeeLanguage:
        language = EmployeeLanguage.objects.get(id=self.kwargs["pk_lang"])
        return language


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
