from django.test import TestCase,Client
from django.urls import reverse,resolve
from ..views import *


class TestMatchJobAppViews(TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        cls.client = Client()

    @classmethod
    def tearDownClass(cls) -> None:
        del cls.client


    def test_get_view_home(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code,200)

    def test_get_view_registration_employee(self):
        response = self.client.get(reverse("registration_choice"))
        self.assertEqual(response.status_code,200)
    def test_get_view_registration_employer(self):
        response = self.client.get(reverse("registration_employee"))
        self.assertEqual(response.status_code,200)
    def test_get_view_login(self):
        response = self.client.get(reverse("registration_employer"))
        self.assertEqual(response.status_code,200)
    def test_get_view_logout(self):
        response = self.client.get(reverse("login"))
        self.assertEqual(response.status_code,200)
    def test_get_view_employee_profile(self):
        response = self.client.get(reverse("logout"))
        self.assertEqual(response.status_code,200)
    def test_get_view_employer_profile(self):
        response = self.client.get(reverse("employee_profile",))
        self.assertEqual(response.status_code,200)
    def test_get_view_employee_profile_update(self):
        response = self.client.get(reverse("employer_profile",))
        self.assertEqual(response.status_code,200)
    def test_get_view_employer_profile_update(self):
        response = self.client.get(reverse("employee_profile_update",))
        self.assertEqual(response.status_code,200)
    def test_get_view_employee_add_language(self):
        response = self.client.get(reverse("employer_profile_update",))
        self.assertEqual(response.status_code,200)
    def test_get_view_employee_language_update(self):
        response = self.client.get(reverse("employee_add_language",))
        self.assertEqual(response.status_code,200)
    def test_get_view_employee_language_delete(self):
        response = self.client.get(reverse("employee_language_update",))
        self.assertEqual(response.status_code,200)
    def test_get_view_employee_add_job(self):
        response = self.client.get(reverse("employee_language_delete",))
        self.assertEqual(response.status_code,200)
    def test_get_view_employee_job_update(self):
        response = self.client.get(reverse("employee_add_job",))
        self.assertEqual(response.status_code,200)
    def test_get_view_employee_job_delete(self):
        response = self.client.get(reverse("employee_job_update",))
        self.assertEqual(response.status_code,200)
    def test_get_view_employee_add_target(self):
        response = self.client.get(reverse("employee_job_delete",))
        self.assertEqual(response.status_code,200)
