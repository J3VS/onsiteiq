from rest_framework import serializers


class ApplicantSerializer(serializers.Serializer):
    first_name = serializers.CharField(
        max_length=50, required=True, allow_blank=False, allow_null=False
    )
    last_name = serializers.CharField(
        max_length=50, required=True, allow_blank=False, allow_null=False
    )
    email = serializers.EmailField(required=True, allow_blank=False, allow_null=False)


class ApplicantNoteSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, allow_blank=False, allow_null=False)
