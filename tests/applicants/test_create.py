from django.contrib.auth.models import Permission
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from tests.utils import AuthenticatedTestCase


class UnauthenticatedApplicantsTests(APITestCase):
    def test_create_applicant_unauthorized(self):
        create_applicant_url = reverse('applicants:create-applicant')
        data = {'username': 'Applicant1'}
        response = self.client.post(create_applicant_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedApplicantsTests(AuthenticatedTestCase):
    def test_create_applicant_authorized_but_unpermitted(self):
        data = {'username': 'Applicant1'}
        response = self.post('applicants:create-applicant', data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_bad_applicant(self):
        permission = Permission.objects.get(codename='can_add_applicant')
        self.user.user_permissions.add(permission)
        self.user.save()
        data = {'username': 'Applicant1'}
        response = self.post('applicants:create-applicant', data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_applicant(self):
        permission = Permission.objects.get(codename='can_add_applicant')
        self.user.user_permissions.add(permission)
        self.user.save()
        data = {'first_name': 'test', 'last_name': 'applicant', 'email': "test.applicant@email.com"}
        response = self.post('applicants:create-applicant', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response.data['applicant_id'])
