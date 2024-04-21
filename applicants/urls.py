from django.urls import path

from applicants.views import ApplicantView, ApproveApplicantView, RejectApplicantView

urlpatterns = [
    path("<str:applicant_id>", ApplicantView.as_view()),
    path("<str:applicant_id>/approve", ApproveApplicantView.as_view()),
    path("<str:applicant_id>/reject", RejectApplicantView.as_view()),
    path("<str:applicant_id>/notes", RejectApplicantView.as_view()),
]
