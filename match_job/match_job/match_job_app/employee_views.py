from typing import Any, Dict
from django.shortcuts import redirect
from django.forms.models import BaseModelForm
from django.http import HttpRequest, HttpResponse
from django.http.response import HttpResponse, HttpResponseRedirect
from django.views.generic import (
    CreateView,
    DeleteView,
    UpdateView,
    DetailView,
    ListView,
    RedirectView
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.decorators import method_decorator
from .decorators import checking_role
from .forms import (
    EmployeeJobTarget,
    UpdateBaseInformationEmployeeForm,
    CreateEmployeeLanguageForm,
    EditEmployeeLanguageForm,
    CreateEmployeeJobForm,
    AddEmployeeJobTarget
    )
from .models import (
    Employee,
    EmployeeJob,
    EmployeeLanguage,
    EmployeeJobTarget
    )

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
    

class ShowEmployeesView(LoginRequiredMixin,ListView):
    login_url = "login"
    template_name = "show_employees.html"
    context_object_name = 'employees'
    paginate_by = 6
    queryset = Employee.objects.all()
    pk_url_kwarg = "target_filter"

    def get_queryset(self) -> QuerySet[Any]:
        queryset = super().get_queryset()   
        try:
            target_filter = self.kwargs['target_filter']
        except:
            return queryset
        queryset = Employee.objects.filter(target__target_name__icontains=target_filter)
        return queryset
    
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        target_filter = self.request.POST.get('target_filter')
        target_filter = target_filter.lower()
        return redirect('show_employees_filtered',target_filter)
        


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
    
