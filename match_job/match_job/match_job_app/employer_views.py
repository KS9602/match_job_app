from typing import Any,Dict
from django.http import  HttpResponse
from django.http.response import HttpResponse
from django.views.generic import (
    CreateView,
    UpdateView,
    DetailView,
)
from .forms import *
from .models import *
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.decorators import method_decorator
from .decorators import checking_role





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
    