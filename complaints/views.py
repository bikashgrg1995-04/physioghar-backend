from rest_framework import generics, permissions

from .models import Complaint
from .serializers import ComplaintSerializer


class ComplaintListCreateView(generics.ListCreateAPIView):
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        therapist_profile = self.request.user.therapist_profile

        return Complaint.objects.filter(
            therapist=therapist_profile,
        ).order_by("-created_at")

    def perform_create(self, serializer):
        therapist_profile = self.request.user.therapist_profile

        serializer.save(
            therapist=therapist_profile,
        )


class ComplaintDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ComplaintSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        therapist_profile = self.request.user.therapist_profile

        return Complaint.objects.filter(
            therapist=therapist_profile,
        )