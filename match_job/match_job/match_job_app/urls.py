from django.urls import path
from .views import *


urlpatterns = [
    path('init_app',init_app),
    path('',HomeView.as_view(),name='home'),
    path('choice_role',ChoiceRoleView.as_view(),name='registration_choice'),
    path('registration_employee',RegistrationEmployeeView.as_view(),name='registration_employee'),
    path('registration_employer',RegistrationEmployerView.as_view(),name='registration_employer'),
    path('login',LoginView.as_view(),name='login'),
    path('logout',LogoutView.as_view(),name='logout'),

    path('employee_profile/<int:pk>',EmployeeProfile.as_view(),name='employee_profile'),
    path('employer_profile/<int:pk>',EmployerProfile.as_view(),name='employer_profile'),
    path('employee_profile/<int:pk>/update_information',EditBaseInformationEmployeeView.as_view(),name='employee_profile_update'),
    path('employer_profile/<int:pk>/update_information',EditBaseInformationEmployerView.as_view(),name='employer_profile_update'),
    path('employer_profile/<int:pk>/add_language',AddLanguageView.as_view(),name='employee_add_language'),
    path('employer_profile/<int:pk>/update_language/<int:pk_lang>',EditLanguageView.as_view(),name='employee_language_update'),
    path('employer_profile/<int:pk>/delete_language/<int:pk_lang>',DeleteLanguageView.as_view(),name='employee_language_delete'),
    path('employer_profile/<int:pk>/add_job',AddJobView.as_view(),name='employee_add_job'),
    
]
