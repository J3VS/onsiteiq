from datetime import datetime
from dataclasses import dataclass

from applicants.models import ApplicantNoteModel, ApplicantModel


@dataclass
class Note:
    text: str
    created_by: str
    created_at: datetime

    @staticmethod
    def make_from(note_model: ApplicantNoteModel):
        return Note(
            text=note_model.note,
            created_by=note_model.user.username,
            created_at=note_model.created,
        )


@dataclass
class Applicant:
    id: str
    first_name: str
    last_name: str
    email: str
    status: str
    notes: list[Note]

    @staticmethod
    def make_from(applicant: ApplicantModel, notes: list[ApplicantNoteModel]):
        sorted_notes = sorted(notes, key=lambda n: n.created)
        return Applicant(
            id=applicant.pk,
            first_name=applicant.first_name,
            last_name=applicant.last_name,
            email=applicant.email,
            status=ApplicantModel.STATUSES[applicant.status],
            notes=[Note.make_from(note) for note in sorted_notes],
        )
