from django.db import models

from accounts.models import TherapistProfile


class Complaint(models.Model):
    class Category(models.TextChoices):
        PATIENT = "patient", "Patient Issue"
        BOOKING = "booking", "Booking Issue"
        PAYMENT = "payment", "Payment Issue"
        TECHNICAL = "technical", "Technical Issue"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        RESOLVED = "resolved", "Resolved"

    therapist = models.ForeignKey(
        TherapistProfile,
        on_delete=models.CASCADE,
        related_name="complaints",
    )

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
        default=Category.OTHER,
    )

    subject = models.CharField(max_length=255)
    description = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject