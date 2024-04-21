from rest_framework.test import APITestCase
from django.urls import reverse

from authentication.models import User


class AuthenticatedTestCase(APITestCase):
    def setUp(self):
        login_url = reverse('authentication:login')
        self.user = User.objects.create_user(username="test", email="test@test.com", password="test")
        self.user.save()
        response = self.client.post(login_url, {'username': "test", 'password': "test"}, format='json')
        self.token = response.data['token']

    def headers(self):
        return {'Authorization': f"Token {self.token}"}

    def get(self, url_name: str):
        url = reverse(url_name)
        return self.client.get(url, format='json', headers=self.headers())

    def post(self, url_name: str, data):
        url = reverse(url_name)
        return self.client.post(url, data, format='json', headers=self.headers())

    def put(self, url_name: str, data):
        url = reverse(url_name)
        return self.client.put(url, data, format='json', headers=self.headers())
