from django.db import models

from onsiteiq.models import BaseModel
from authentication.models import User
from django.contrib.auth.models import Permission


class Status:
    PENDING = 0
    APPROVED = 1
    REJECTED = 2


class ApplicantModel(BaseModel):
    STATUSES = {
        Status.PENDING: 'Pending',
        Status.APPROVED: 'Approved',
        Status.REJECTED: 'Rejected'
    }

    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=100)
    status = models.IntegerField(default=0, choices=STATUSES)

    class Meta:
        permissions = [
            ("can_add_applicant", "Can create an applicant"),
            ("can_view_applicants", "Can view applicants"),
            ("can_change_applicant_status", "Can approve or reject applicants"),
            ("can_add_applicant_note", "Can add notes to applicants"),
        ]


class ApplicantNoteModel(BaseModel):
    note = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    applicant = models.ForeignKey(ApplicantModel, on_delete=models.CASCADE)
    created = models.DateTimeField()
