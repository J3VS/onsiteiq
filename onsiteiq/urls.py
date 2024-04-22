from django.urls import path, include

from applicants import urls as applicant_urls
from authentication import urls as authentication_urls

urlpatterns = [
    path("authentication/", include(authentication_urls, namespace="authentication")),
    path("applicants/", include(applicant_urls, namespace="applicants")),
]
