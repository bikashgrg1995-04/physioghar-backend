
from django.shortcuts import get_object_or_404

from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Patient, PatientNote
from .serializers import (
    PatientDetailSerializer,
    PatientListSerializer,
    PatientNoteSerializer,
)


class PatientListView(generics.ListAPIView):
    serializer_class = PatientListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(
            therapist=self.request.user,
        )


class PatientDetailView(generics.RetrieveAPIView):
    serializer_class = PatientDetailSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Patient.objects.filter(
            therapist=self.request.user,
        )


class PatientNoteListCreateView(
    generics.ListCreateAPIView,
):
    serializer_class = PatientNoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientNote.objects.filter(
            patient_id=self.kwargs["patient_id"],
            patient__therapist=self.request.user,
        ).select_related(
            "patient",
            "therapist",
        )

    def perform_create(self, serializer):
        patient = get_object_or_404(
            Patient,
            id=self.kwargs["patient_id"],
            therapist=self.request.user,
        )

        serializer.save(
            patient=patient,
            therapist=self.request.user,
        )


class PatientNoteDetailView(
    generics.RetrieveUpdateDestroyAPIView,
):
    serializer_class = PatientNoteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientNote.objects.filter(
            patient_id=self.kwargs["patient_id"],
            patient__therapist=self.request.user,
        )

