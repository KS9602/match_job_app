from django.test import TestCase
from django.urls import reverse, resolve
from ..urls import urlpatterns
from ..views import *


class MatchJobUrlsTests(TestCase):
    def test_url_name_home(self):
        url = reverse("home")
        self.assertEqual(resolve(url).func.view_class, HomeView)

    def test_url_name_registration_choice(self):
        url = reverse("registration_choice")
        self.assertEqual(resolve(url).func.view_class, ChoiceRoleView)

    def test_url_name_registration_employee(self):
        url = reverse("registration_employee")
        self.assertEqual(resolve(url).func.view_class, RegistrationEmployeeView)

    def test_url_name_registration_employer(self):
        url = reverse("registration_employer")
        self.assertEqual(resolve(url).func.view_class, RegistrationEmployerView)

    def test_url_name_login(self):
        url = reverse("login")
        self.assertEqual(resolve(url).func.view_class, LoginView)

    def test_url_name_logout(self):
        url = reverse("logout")
        self.assertEqual(resolve(url).func.view_class, LogoutView)

    def test_url_name_employee_profile(self):
        url = reverse("employee_profile", args=[1])
        self.assertEqual(resolve(url).func.view_class, EmployeeProfile)

    def test_url_name_employer_profile(self):
        url = reverse("employer_profile", args=[1])
        self.assertEqual(resolve(url).func.view_class, EmployerProfile)

    def test_url_name_employee_profile_update(self):
        url = reverse("employee_profile_update", args=[1])
        self.assertEqual(resolve(url).func.view_class, EditBaseInformationEmployeeView)

    def test_url_name_employer_profile_update(self):
        url = reverse("employer_profile_update", args=[1])
        self.assertEqual(resolve(url).func.view_class, EditBaseInformationEmployerView)

    def test_url_name_employee_add_language(self):
        url = reverse("employee_add_language", args=[1])
        self.assertEqual(resolve(url).func.view_class, AddLanguageView)

    def test_url_name_employee_language_update(self):
        url = reverse("employee_language_update", args=[1, 1])
        self.assertEqual(resolve(url).func.view_class, EditLanguageView)

    def test_url_name_employee_language_delete(self):
        url = reverse("employee_language_delete", args=[1, 1])
        self.assertEqual(resolve(url).func.view_class, DeleteLanguageView)

    def test_url_name_employee_add_job(self):
        url = reverse("employee_add_job", args=[1])
        self.assertEqual(resolve(url).func.view_class, AddJobView)

    def test_url_name_employee_job_update(self):
        url = reverse("employee_job_update", args=[1, 1])
        self.assertEqual(resolve(url).func.view_class, EditJobView)

    def test_url_name_employee_job_delete(self):
        url = reverse("employee_job_delete", args=[1, 1])
        self.assertEqual(resolve(url).func.view_class, DeleteJobView)

    def test_url_name_employee_add_target(self):
        url = reverse("employee_add_target", args=[1])
        self.assertEqual(resolve(url).func.view_class, AddEmployeeTargetJob)


class MatchJobUrlsTests(TestCase):
    pass
