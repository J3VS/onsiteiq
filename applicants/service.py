from datetime import datetime

from applicants.data import Applicant
from applicants.exceptions import ApplicantNotFound
from applicants.models import ApplicantModel, Status, ApplicantNoteModel
from authentication.models import User


class ApplicantService:
    @staticmethod
    def create_applicant(applicant: Applicant) -> str:
        model = ApplicantModel(first_name=applicant['first_name'],
                               last_name=applicant['last_name'],
                               email=applicant['last_name'])
        model.save()
        return model.pk

    @staticmethod
    def get_applicant(applicant_id: str) -> Applicant:
        try:
            applicant_model = ApplicantModel.objects.get(pk=applicant_id)
            return Applicant(first_name=applicant_model.first_name,
                             last_name=applicant_model.last_name,
                             email=applicant_model.email,
                             status=applicant_model.status)
        except ApplicantModel.DoesNotExist:
            raise ApplicantNotFound()

    @staticmethod
    def approve(applicant_id: str):
        ApplicantService.set_status(applicant_id, Status.APPROVED)

    @staticmethod
    def reject(applicant_id: str):
        ApplicantService.set_status(applicant_id, Status.REJECTED)

    @staticmethod
    def set_status(applicant_id: str, status: Status):
        try:
            applicant_model = ApplicantModel.objects.get(pk=applicant_id)
            applicant_model.status = status
            applicant_model.save()
        except ApplicantModel.DoesNotExist:
            raise ApplicantNotFound()

    @staticmethod
    def add_note(applicant_id: str, note: str, user: User):
        try:
            applicant_model = ApplicantModel.objects.get(pk=applicant_id)
            applicant_note = ApplicantNoteModel(applicant=applicant_model,
                                                note=note,
                                                user=user,
                                                created=datetime.now())
            applicant_note.save()
            return applicant_note.pk
        except ApplicantModel.DoesNotExist:
            raise ApplicantNotFound()
