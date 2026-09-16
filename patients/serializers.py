from rest_framework import serializers

from .models import Patient
from .models import PatientNote


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

class PatientNoteSerializer(serializers.ModelSerializer): 
    class Meta: 
        model = PatientNote 
        fields = ( 
            "id", 
            "patient", 
            "therapist", 
            "content", 
            "created_at", 
            "updated_at", 
        ) 
        read_only_fields = ( 
            "id", 
            "patient", 
            "therapist",
            "created_at", 
            "updated_at", 
        ) 

        def validate_content(self, value): 
            value = value.strip() 

            if not value: 
                raise serializers.ValidationError( 
                    "Note cannot be empty." 
                ) 

            return value