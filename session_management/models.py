
from django.conf import settings
from django.db import models


class SessionStatus(models.TextChoices):
    REQUESTED = "requested", "Requested"
    UPCOMING = "upcoming", "Upcoming"
    COMPLETED = "completed", "Completed"
    CANCELLED = "cancelled", "Cancelled"


class Session(models.Model):
    therapist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="therapy_sessions",
    )

    patient = models.ForeignKey(
        "patients.Patient",
        on_delete=models.CASCADE,
        related_name="sessions",
    )

        
    schedule_slot = models.ForeignKey(
        "schedules.ScheduleSlot",
        on_delete=models.PROTECT,
        related_name="sessions",
    )


    treatment = models.CharField(
        max_length=255,
    )

    location = models.CharField(
        max_length=255,
    )

    status = models.CharField(
        max_length=20,
        choices=SessionStatus.choices,
        default=SessionStatus.REQUESTED,
    )

    notes = models.TextField(
        blank=True,
        default="",
    )

    cancellation_reason = models.TextField(
        blank=True,
        default="",
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "schedule_slot__date",
            "schedule_slot__time",
        ]

    def __str__(self):
        return (
            f"{self.patient} - "
            f"{self.schedule_slot.date} "
            f"{self.schedule_slot.time} - "
            f"{self.status}"
        )
