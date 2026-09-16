from rest_framework import serializers

from .models import Patient


class PatientListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
            "id",
            "name",
            "age",
            "gender",
            "phone",
            "condition",
        )


class PatientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Patient
        fields = (
            "id",
            "name",
            "age",
            "gender",
            "phone",
            "email",
            "address",
            "condition",
            "created_at",
            "updated_at",
        )