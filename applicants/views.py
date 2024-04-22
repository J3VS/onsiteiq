from dataclasses import asdict
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from applicants.exceptions import ApplicantNotFound
from applicants.permissions import (
    AddApplicantPermission,
    ViewApplicantPermission,
    ChangeApplicantStatusPermission,
    AddApplicantNotesPermission,
)
from applicants.serializers import ApplicantSerializer, ApplicantNoteSerializer
from applicants.service import ApplicantService
from rest_framework import status


@api_view(["POST"])
@permission_classes((IsAuthenticated, AddApplicantPermission))
def create_applicant(request: Request, format=None):
    applicant_serializer = ApplicantSerializer(data=request.data)
    if not applicant_serializer.is_valid():
        return Response(
            {"message": applicant_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )

    applicant = applicant_serializer.validated_data
    applicant_id: str = ApplicantService.create_applicant(**applicant)
    return Response({"applicant_id": applicant_id})


@api_view(["GET"])
@permission_classes((IsAuthenticated, ViewApplicantPermission))
def view_applicant(request: Request, applicant_id: str, format=None):
    try:
        return Response(asdict(ApplicantService.get_applicant(applicant_id)))
    except ApplicantNotFound:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes((IsAuthenticated, ChangeApplicantStatusPermission))
def approve_applicant(request: Request, applicant_id: str, format=None):
    try:
        ApplicantService.approve(applicant_id)
        return Response(status=status.HTTP_200_OK)
    except ApplicantNotFound:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes((IsAuthenticated, ChangeApplicantStatusPermission))
def reject_applicant(request: Request, applicant_id: str, format=None):
    try:
        ApplicantService.reject(applicant_id)
        return Response(status=status.HTTP_200_OK)
    except ApplicantNotFound:
        return Response(status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes((IsAuthenticated, AddApplicantNotesPermission))
def add_applicant_note(request: Request, applicant_id: str):
    note_serializer = ApplicantNoteSerializer(data=request.data)
    if not note_serializer.is_valid():
        return Response(
            {"message": note_serializer.errors}, status=status.HTTP_400_BAD_REQUEST
        )
    body = note_serializer.validated_data
    note_text = body["text"]

    try:
        applicant_note_id: str = ApplicantService.add_note(
            applicant_id, note_text, request.user
        )
        return Response({"applicant_note_id": applicant_note_id})
    except ApplicantNotFound:
        return Response(status=status.HTTP_404_NOT_FOUND)
