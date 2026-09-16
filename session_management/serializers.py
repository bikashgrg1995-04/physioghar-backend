
from rest_framework import serializers

from schedules.models import ScheduleSlot

from .models import Session


class SessionSerializer(serializers.ModelSerializer):
    patient_name = serializers.CharField(
        source="patient.name",
        read_only=True,
    )

    schedule_date = serializers.DateField(
        source="schedule_slot.date",
        read_only=True,
    )

    schedule_time = serializers.TimeField(
        source="schedule_slot.time",
        read_only=True,
    )

    session_id = serializers.IntegerField(
        source="id",
        read_only=True,
    )

    class Meta:
        model = Session
        fields = (
            "id",
            "session_id",
            "patient",
            "patient_name",
            "schedule_slot",
            "schedule_date",
            "schedule_time",
            "treatment",
            "location",
            "status",
            "notes",
            "cancellation_reason",
            "created_at",
            "updated_at",
        )

        read_only_fields = (
            "id",
            "session_id",
            "patient_name",
            "schedule_date",
            "schedule_time",
            "status",
            "created_at",
            "updated_at",
        )

    def validate_schedule_slot(
        self,
        schedule_slot,
    ):
        request = self.context.get("request")

        if (
            request is None
            or not request.user.is_authenticated
        ):
            raise serializers.ValidationError(
                "Authentication is required."
            )

        if schedule_slot.therapist_id != request.user.id:
            raise serializers.ValidationError(
                "You can only use your own schedule slots."
            )

        if schedule_slot.status != "open":
            raise serializers.ValidationError(
                "Only open schedule slots can be booked."
            )

        if hasattr(schedule_slot, "session"):
            raise serializers.ValidationError(
                "This schedule slot already has a session."
            )

        return schedule_slot
