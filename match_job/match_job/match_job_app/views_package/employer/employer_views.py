from typing import Any, Dict
from django.views.generic import (
    UpdateView,
    DetailView,
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.utils.decorators import method_decorator
from match_job_app.decorators.checking_role import checking_role
from match_job_app.forms.employer_froms import UpdateBaseInformationEmployerForm
from match_job_app.models import Employer, JobPost


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


class PublicEmployerProfileView(LoginRequiredMixin, DetailView):
    login_url = "login"
    template_name = "public_employer_profile.html"
    context_object_name = "employer"
    model = Employer

    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user = Employer.objects.get(id=self.kwargs["pk"])
        context["employer"] = user
        context["job_posts"] = JobPost.objects.filter(employer=user)

        return context
