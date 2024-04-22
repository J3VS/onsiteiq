from rest_framework import serializers


class ApplicantSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50, required=True)
    last_name = serializers.CharField(max_length=50, required=True)
    email = serializers.EmailField(required=True)


class ApplicantNoteSerializer(serializers.Serializer):
    text = serializers.CharField(required=True, allow_blank=False, allow_null=False)
