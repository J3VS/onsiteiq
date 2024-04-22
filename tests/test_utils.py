from rest_framework.test import APITestCase
from django.urls import reverse
from datetime import datetime, timedelta
from authentication.models import User
from onsiteiq.time import now


def assert_since(
    test_case: APITestCase,
    time: datetime,
    days: int = 0,
    seconds: int = 0,
    microseconds: int = 0,
    milliseconds: int = 0,
    minutes: int = 0,
    hours: int = 0,
    weeks: int = 0,
):
    dt_now = now()
    ago = dt_now - timedelta(
        days=days,
        seconds=seconds,
        microseconds=microseconds,
        milliseconds=milliseconds,
        minutes=minutes,
        hours=hours,
        weeks=weeks,
    )
    test_case.assertGreater(time, ago)
    test_case.assertLess(time, dt_now)


class AuthenticatedTestCase(APITestCase):
    def setUp(self):
        login_url = reverse("authentication:login")
        self.user = User.objects.create_user(
            username="test", email="test@test.com", password="test"
        )
        self.user.save()
        response = self.client.post(
            login_url, {"username": "test", "password": "test"}, format="json"
        )
        self.token = response.data["token"]

    def headers(self):
        return {"Authorization": f"Token {self.token}"}

    def get(self, url_name: str, url_args: list[str] = None):
        url = reverse(url_name, args=url_args)
        return self.client.get(url, format="json", headers=self.headers())

    def post(self, url_name: str, data: dict[str, any], url_args: list[str] = None):
        url = reverse(url_name, args=url_args)
        return self.client.post(url, data, format="json", headers=self.headers())

    def put(self, url_name: str, data: dict[str, any], url_args: list[str] = None):
        url = reverse(url_name, args=url_args)
        return self.client.put(url, data, format="json", headers=self.headers())
