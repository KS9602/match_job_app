from typing import Any
from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpRequest
from django.views.generic import (
    CreateView,
    UpdateView,
    View
)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models.query import QuerySet
from django.urls import reverse
from django.utils.decorators import method_decorator
from ..decorators import checking_role

from .employer_froms import CreateJobPostForm
from ..models import Employer, JobPost,JobPostFeature,JobPostRequirementOptional,JobPostRequirementMustHave


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


class AddJobRequirementFeatureView(View):

    template_name = 'add_job_requirement_feature.html'

    def get(self, request: HttpRequest, *args: str, **kwargs: Any) -> HttpResponse:
        return render(request,self.template_name)

    def post(self, request, *args, **kwargs):
        pk = self.kwargs["pk"]
        post = JobPost.objects.get(id=self.kwargs['pk_post']) 
        form = self.request.POST
        print(form)
        features = [JobPostFeature(feature=form[key],job_post=post) for key in form.keys() 
                    if 'feature' in key and form[key] != '' ]
        requirements_must = [JobPostRequirementMustHave(requirement=form[key],job_post=post) for key in form.keys() 
                        if 'requirement_must_have' in key and form[key] != '' ]
        requirements_optional = [JobPostRequirementOptional(requirement=form[key],job_post=post) for key in form.keys() 
                        if 'requirement_optional' in key and form[key] != '' ]

        JobPostFeature.objects.bulk_create(features)
        JobPostRequirementMustHave.objects.bulk_create(requirements_must)
        JobPostRequirementOptional.objects.bulk_create(requirements_optional)
        return redirect("employer_profile", pk)
    

    # DODAC IMPORTANCE