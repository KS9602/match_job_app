from match_job_app.views_package.employer.employer_views import (
EmployerProfileView,
EditBaseInformationEmployerView,
PublicEmployerProfileView,
)
from match_job_app.views_package.employer.employer_job_post_views import (
AddJEmployerobPostView,
EditEmployerJobPostView,
AddJobRequirementFeatureView,
JobPostView,
)
from match_job_app.views_package.employee.employee_views import (
EmployeeProfile,
EditBaseInformationEmployeeView,
ShowEmployeesView,
PublicEmployeeProfileView,
)
from match_job_app.views_package.employee.job_target_views import(
AddEmployeeTargetJobView,
DeleteEmployeeTargetView,
)
from match_job_app.views_package.employee.job_views import (
AddJobView,
EditJobView,
DeleteJobView,
)
from match_job_app.views_package.employee.language_views import (
AddLanguageView,
EditLanguageView,
DeleteLanguageView
)
from match_job_app.views_package.main_views.main_views import (
HomeView,
)
from match_job_app.views_package.authentication.authentication_views import  (
ChoiceRoleView,
RegistrationEmployeeView,
RegistrationEmployerView,
LoginView,
LogoutView,
)
from django.views.generic import TemplateView

def init_app(request):
    if Group.objects.all().count() < 2:
        employee_group = Group(name="employee")
        employer_group = Group(name="employer")
        employee_group.save()
        employer_group.save()
    return redirect("home")

class TesT(TemplateView):
    template_name = "test.html"




