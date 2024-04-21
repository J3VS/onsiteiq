from django.urls import path, include

from applicants import urls as applicant_urls
from authentication import urls as auth_urls

urlpatterns = [
    path('applicants', include(applicant_urls, namespace='applicants')),
    path('authentication', include(auth_urls, namespace='authentication')),
]
