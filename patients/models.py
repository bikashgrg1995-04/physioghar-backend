
from django.conf import settings
from django.db import models


class Patient(models.Model):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"

    therapist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patients",
    )

    name = models.CharField(
        max_length=150,
    )

    age = models.PositiveIntegerField()

    gender = models.CharField(
        max_length=20,
        choices=Gender.choices,
    )

    phone = models.CharField(
        max_length=20,
        blank=True,
    )

    email = models.EmailField(
        blank=True,
    )

    address = models.CharField(
        max_length=255,
        blank=True,
    )

    condition = models.CharField(
        max_length=255,
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class PatientNote(models.Model):
    therapist = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="patient_notes",
    )

    patient = models.ForeignKey(
        "Patient",
        on_delete=models.CASCADE,
        related_name="notes",
    )

    content = models.TextField()

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return (
            f"{self.patient.name} - "
            f"Note {self.id}"
        )

