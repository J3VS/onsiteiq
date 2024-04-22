from django.urls import path

from applicants.views import (
    create_applicant,
    view_applicant,
    approve_applicant,
    reject_applicant,
    add_applicant_note,
)

app_name = "applicants"

urlpatterns = [
    path("", create_applicant, name="create-applicant"),
    path("<str:applicant_id>", view_applicant, name="view-applicant"),
    path("<str:applicant_id>/approve", approve_applicant, name="approve-applicant"),
    path("<str:applicant_id>/reject", reject_applicant, name="reject-applicant"),
    path("<str:applicant_id>/notes", add_applicant_note, name="add-applicant-note"),
]
