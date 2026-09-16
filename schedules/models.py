
from django.conf import settings
from django.db import models


class ScheduleSlot(models.Model):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        BOOKED = "booked", "Booked"
        BLOCKED = "blocked", "Blocked"

    therapist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="schedule_slots",
    )

    date = models.DateField()

    time = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.OPEN,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = [
            "date",
            "time",
        ]
        constraints = [
            models.UniqueConstraint(
                fields=[
                    "therapist",
                    "date",
                    "time",
                ],
                name="unique_therapist_schedule_slot",
            ),
        ]

    def __str__(self):
        return (
            f"{self.therapist} - "
            f"{self.date} - "
            f"{self.time}"
        )

