from django.contrib.auth.models import Permission
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from applicants.models import ApplicantModel
from tests.applicants.applicant_utils import create_test_applicant
from tests.test_utils import AuthenticatedTestCase


class UnauthenticatedRejectApplicantTests(APITestCase):
    def test_reject_applicant_unauthorized(self):
        applicant_id = create_test_applicant()
        reject_applicant_url = reverse(
            "applicants:reject-applicant", args=[applicant_id]
        )
        response = self.client.post(reject_applicant_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedRejectApplicantTests(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.applicant_id = create_test_applicant()

    def test_reject_applicant_authorized_but_unpermitted(self):
        response = self.post(
            "applicants:reject-applicant", {}, url_args=[self.applicant_id]
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_reject_applicant(self):
        permission = Permission.objects.get(codename="can_change_applicant_status")
        self.user.user_permissions.add(permission)
        self.user.save()

        applicant_model = ApplicantModel.objects.get(pk=self.applicant_id)
        self.assertEqual(ApplicantModel.STATUSES[applicant_model.status], "Pending")

        response = self.post(
            "applicants:reject-applicant", {}, url_args=[self.applicant_id]
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        applicant_model = ApplicantModel.objects.get(pk=self.applicant_id)
        self.assertEqual(ApplicantModel.STATUSES[applicant_model.status], "Rejected")
