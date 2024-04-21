from dataclasses import dataclass

from applicants.models import ApplicantModel


@dataclass
class Applicant:
    first_name: str
    last_name: str
    email: str
    status: str
