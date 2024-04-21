from rest_framework import serializers


class ApplicantSerializer(serializers.Serializer):
    first_name = serializers.CharField(max_length=50)
    last_name = serializers.CharField(max_length=50)
    email = serializers.EmailField()


class ApplicantNoteSerializer(serializers.Serializer):
    applicant_id = serializers.CharField(max_length=50)
    text = serializers.CharField()
