from django.urls import path

from applicants import urls as applicant_urls
from auth import urls as auth_urls

urlpatterns = [
    path('applicants/', applicant_urls),
    path('auth/', auth_urls),
]
