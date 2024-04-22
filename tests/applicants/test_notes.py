from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from applicants.models import ApplicantNoteModel
from tests.applicants.applicant_utils import create_test_applicant
from tests.test_utils import AuthenticatedTestCase, assert_since


class UnauthenticatedAddApplicantNoteTests(APITestCase):
    def test_add_applicant_note_unauthorized(self):
        applicant_id = create_test_applicant()
        add_applicant_note_url = reverse(
            "applicants:add-applicant-note", args=[applicant_id]
        )
        response = self.client.post(add_applicant_note_url, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedAddApplicantNoteTests(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.applicant_id = create_test_applicant()

    def test_add_applicant_note_authorized_but_unpermitted(self):
        response = self.post(
            "applicants:add-applicant-note", {}, url_args=[self.applicant_id]
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PermittedAddApplicantNoteTests(AuthenticatedTestCase):
    def setUp(self):
        super().setUp()
        self.applicant_id = create_test_applicant()
        permission = Permission.objects.get(codename="can_add_applicant_note")
        self.user.user_permissions.add(permission)
        self.user.save()

    def test_note_no_body(self):
        response = self.post(
            "applicants:add-applicant-note", {}, url_args=[self.applicant_id]
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_note_no_note_text(self):
        response = self.post(
            "applicants:add-applicant-note",
            {"text": None},
            url_args=[self.applicant_id],
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_note_empty_note_text(self):
        response = self.post(
            "applicants:add-applicant-note", {"text": ""}, url_args=[self.applicant_id]
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_add_note(self):
        note_text = "A test note"
        response = self.post(
            "applicants:add-applicant-note",
            {"text": note_text},
            url_args=[self.applicant_id],
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        applicant_notes = ApplicantNoteModel.objects.filter(
            applicant_id=self.applicant_id
        )
        self.assertEqual(len(applicant_notes), 1)

        applicant_note = applicant_notes[0]

        self.assertEqual(applicant_note.user.username, "test")
        self.assertEqual(applicant_note.note, note_text)

        assert_since(self, applicant_note.created, seconds=5)
