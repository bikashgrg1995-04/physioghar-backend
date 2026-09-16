
from rest_framework import generics, mixins
from rest_framework.permissions import IsAuthenticated

from .models import ScheduleSlot
from .serializers import ScheduleSlotSerializer


class ScheduleSlotListCreateView(
    generics.ListCreateAPIView,
):
    serializer_class = ScheduleSlotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = ScheduleSlot.objects.filter(
            therapist=self.request.user,
        )

        date = self.request.query_params.get("date")

        if date:
            queryset = queryset.filter(
                date=date,
            )

        return queryset

    def perform_create(self, serializer):
        serializer.save(
            therapist=self.request.user,
        )


class ScheduleSlotUpdateDeleteView(
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    generics.GenericAPIView,
):
    serializer_class = ScheduleSlotSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return ScheduleSlot.objects.filter(
            therapist=self.request.user,
        )

    def patch(self, request, *args, **kwargs):
        return self.partial_update(
            request,
            *args,
            **kwargs,
        )

    def delete(self, request, *args, **kwargs):
        return self.destroy(
            request,
            *args,
            **kwargs,
        )

