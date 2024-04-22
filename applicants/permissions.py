from rest_framework.permissions import BasePermission


class AddApplicantPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("applicants.can_add_applicant")


class ViewApplicantPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("applicants.can_view_applicant")


class ChangeApplicantStatusPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("applicants.can_change_applicant_status")


class AddApplicantNotesPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.has_perm("applicants.can_add_applicant_note")
