
from django.urls import path

from .views import (
    PatientDetailView,
    PatientListView,
    PatientNoteDetailView,
    PatientNoteListCreateView,
)

urlpatterns = [
    path(
        "",
        PatientListView.as_view(),
        name="patient-list",
    ),

    path(
        "<int:pk>/",
        PatientDetailView.as_view(),
        name="patient-detail",
    ),

    path(
        "<int:patient_id>/notes/",
        PatientNoteListCreateView.as_view(),
        name="patient-note-list-create",
    ),

    path(
        "<int:patient_id>/notes/<int:pk>/",
        PatientNoteDetailView.as_view(),
        name="patient-note-detail",
    ),
]
