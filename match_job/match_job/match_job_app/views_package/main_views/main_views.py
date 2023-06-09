from typing import Any,Dict
from django.http import HttpRequest,HttpResponse
from django.shortcuts import get_object_or_404
from match_job_app.views_package.view_utils.random_users_roller import RandomUserRoller
from django.views.generic import (
TemplateView
)
from match_job_app.models import (
Employer,
Employee
)

class HomeView(TemplateView):
    template_name = "home.html"


    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)
        user_roller = RandomUserRoller().random_one_eployee_and_employer()
        context["random_users"] = user_roller

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

