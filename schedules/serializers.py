from rest_framework import serializers

from .models import ScheduleSlot


class ScheduleSlotSerializer(
    serializers.ModelSerializer,
):
    session_id = serializers.SerializerMethodField()

    class Meta:
        model = ScheduleSlot
        fields = (
            "id",
            "date",
            "time",
            "status",
            "session_id",
        )
        read_only_fields = (
            "id",
            "session_id",
        )

    def get_session_id(self, obj):
        session = obj.sessions.order_by("-created_at").first()
        return session.id if session else None

    def validate(self, attrs):
        date = attrs.get(
            "date",
            getattr(self.instance, "date", None),
        )

        time = attrs.get(
            "time",
            getattr(self.instance, "time", None),
        )

        if date is not None and time is not None:
            queryset = ScheduleSlot.objects.filter(
                therapist=self.context["request"].user,
                date=date,
                time=time,
            )

            if self.instance is not None:
                queryset = queryset.exclude(
                    pk=self.instance.pk,
                )

            if queryset.exists():
                raise serializers.ValidationError({
                    "time": (
                        "A schedule slot already exists "
                        "for this date and time."
                    ),
                })

        return attrs