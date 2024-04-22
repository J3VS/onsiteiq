from django.contrib.auth.models import Permission
from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status

from applicants.models import ApplicantNoteModel, ApplicantModel
from onsiteiq.time import now
from tests.applicants.applicant_utils import create_test_applicant
from tests.test_utils import AuthenticatedTestCase, assert_since


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

    def test_view_applicant_with_notes(self):
        applicant = ApplicantModel.objects.get(pk=self.applicant_id)
        ApplicantNoteModel.objects.create(
            note="A first note", user=self.user, applicant=applicant, created=now()
        )
        ApplicantNoteModel.objects.create(
            note="A second note", user=self.user, applicant=applicant, created=now()
        )

        permission = Permission.objects.get(codename="can_view_applicant")
        self.user.user_permissions.add(permission)
        self.user.save()
        response = self.get("applicants:view-applicant", url_args=[self.applicant_id])
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        notes = response.data["notes"]

        first_note = notes[0]
        self.assertEqual(first_note["text"], "A first note")
        self.assertEqual(first_note["created_by"], "test")
        assert_since(self, first_note["created_at"], seconds=5)

        second_note = notes[1]
        self.assertEqual(second_note["text"], "A second note")
        self.assertEqual(second_note["created_by"], "test")
        assert_since(self, second_note["created_at"], seconds=5)

        self.assertGreater(second_note["created_at"], first_note["created_at"])
