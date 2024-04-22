from applicants.models import ApplicantModel


def create_test_applicant() -> str:
    applicant = ApplicantModel(
        first_name="test", last_name="applicant", email="test.applicant@email.com"
    )
    applicant.save()
    return applicant.pk
