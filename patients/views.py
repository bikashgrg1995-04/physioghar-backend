from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Patient
from .serializers import (
    PatientDetailSerializer,
    PatientListSerializer,
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

    