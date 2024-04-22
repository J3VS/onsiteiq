from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from applicants.models import ApplicantModel
from tests.test_utils import AuthenticatedTestCase


class UnauthenticatedCreateApplicantTests(APITestCase):
    def test_create_applicant_unauthorized(self):
        create_applicant_url = reverse("applicants:create-applicant")
        data = {"username": "Applicant1"}
        response = self.client.post(create_applicant_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedCreateApplicantTests(AuthenticatedTestCase):
    def test_create_applicant_authorized_but_unpermitted(self):
        data = {"username": "Applicant1"}
        response = self.post("applicants:create-applicant", data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PermittedCreateApplicantTests(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        permission = Permission.objects.get(codename="can_add_applicant")
        self.user.user_permissions.add(permission)
        self.user.save()

    def test_create_bad_applicant(self):
        data = {"username": "Applicant1"}
        response = self.post("applicants:create-applicant", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_applicant_no_first_name(self):
        data = {"last_name": "applicant", "email": "test.applicant@email.com"}
        response = self.post("applicants:create-applicant", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_applicant_no_last_name(self):
        data = {"first_name": "test", "email": "test.applicant@email.com"}
        response = self.post("applicants:create-applicant", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_applicant_no_email(self):
        data = {"first_name": "test", "last_name": "applicant"}
        response = self.post("applicants:create-applicant", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_applicant_bad_email(self):
        data = {"first_name": "test", "last_name": "applicant", "email": "bad-email"}
        response = self.post("applicants:create-applicant", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_applicant_first_name_too_long(self):
        data = {
            "first_name": "testtesttesttesttesttesttesttesttesttesttesttesttes",
            "last_name": "applicant",
            "email": "test.applicant@email.com",
        }
        response = self.post("applicants:create-applicant", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_applicant_last_name_too_long(self):
        data = {
            "first_name": "test",
            "last_name": "applicantapplicantapplicantapplicantapplicantapplic",
            "email": "test.applicant@email.com",
        }
        response = self.post("applicants:create-applicant", data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_applicant(self):
        first_name = "ben"
        last_name = "applicant"
        email = "ben.applicant@email.com"
        data = {
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
        }
        response = self.post("applicants:create-applicant", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        applicant_id = response.data["applicant_id"]
        self.assertIsNotNone(applicant_id)

        applicant = ApplicantModel.objects.get(pk=applicant_id)
        self.assertEquals(applicant.first_name, first_name)
        self.assertEquals(applicant.last_name, last_name)
        self.assertEquals(applicant.email, email)
        self.assertEquals(ApplicantModel.STATUSES[applicant.status], "Pending")
