from django.contrib.auth.models import Permission
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from tests.applicants.applicant_utils import create_test_applicant
from tests.test_utils import AuthenticatedTestCase


class UnauthenticatedViewApplicantTests(APITestCase):
    def test_view_applicant_unauthorized(self):
        applicant_id = create_test_applicant()
        view_applicant_url = reverse("applicants:view-applicant", args=[applicant_id])
        response = self.client.post(view_applicant_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedViewApplicantTests(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.applicant_id = create_test_applicant()

    def test_view_applicant_authorized_but_unpermitted(self):
        response = self.get("applicants:view-applicant", url_args=[self.applicant_id])
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_view_applicant(self):
        permission = Permission.objects.get(codename="can_view_applicant")
        self.user.user_permissions.add(permission)
        self.user.save()
        response = self.get("applicants:view-applicant", url_args=[self.applicant_id])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.data,
            {
                "id": self.applicant_id,
                "first_name": "test",
                "last_name": "applicant",
                "email": "test.applicant@email.com",
                "status": "Pending",
                "notes": [],
            },
        )
