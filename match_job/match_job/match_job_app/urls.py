from django.urls import path
from .views import *


urlpatterns = [
    path("init_app", init_app),
    path("", HomeView.as_view(), name="home"),
    path("choice_role", ChoiceRoleView.as_view(), name="registration_choice"),
    path(
        "registration_employee",
        RegistrationEmployeeView.as_view(),
        name="registration_employee",
    ),
    path(
        "registration_employer",
        RegistrationEmployerView.as_view(),
        name="registration_employer",
    ),
    path("login", LoginView.as_view(), name="login"),
    path("logout", LogoutView.as_view(), name="logout"),
    path(
        "employee_profile/<int:pk>", EmployeeProfile.as_view(), name="employee_profile"
    ),
    path(
        "employer_profile/<int:pk>", EmployerProfileView.as_view(), name="employer_profile"
    ),
    path(
        "employee_profile/<int:pk>/update_information",
        EditBaseInformationEmployeeView.as_view(),
        name="employee_profile_update",
    ),
    path(
        "employer_profile/<int:pk>/update_information",
        EditBaseInformationEmployerView.as_view(),
        name="employer_profile_update",
    ),
    path(
        "employee_profile/<int:pk>/add_language",
        AddLanguageView.as_view(),
        name="employee_add_language",
    ),
    path(
        "employee_profile/<int:pk>/update_language/<int:pk_lang>",
        EditLanguageView.as_view(),
        name="employee_language_update",
    ),
    path(
        "employee_profile/<int:pk>/delete_language/<int:pk_lang>",
        DeleteLanguageView.as_view(),
        name="employee_language_delete",
    ),
    path(
        "employee_profile/<int:pk>/add_job",
        AddJobView.as_view(),
        name="employee_add_job",
    ),
    path(
        "employee_profile/<int:pk>/update_job/<int:pk_job>",
        EditJobView.as_view(),
        name="employee_job_update",
    ),
    path(
        "employee_profile/<int:pk>/delete_job/<int:pk_job>",
        DeleteJobView.as_view(),
        name="employee_job_delete",
    ),
    path(
        "employee_profile/<int:pk>/add_target",
        AddEmployeeTargetJobView.as_view(),
        name="employee_add_target",
    ),
    path(
        "employer_profile/<int:pk>/add_job_post",
        AddJEmployerobPostView.as_view(),
        name="employer_add_job_post",
    ),
    path(
        "employer_profile/<int:pk>/edit_job_post/<int:pk_post>",
        EditEmployerJobPostView.as_view(),
        name="employer_edit_job_post",
    ),
    path("employee_public_profile/<int:pk>",PublicEmployeeProfileView.as_view(),name="employee_public_profile"),
    path("show_employee",ShowEmployeesView.as_view(),name="show_employee"),

]
