
from django.urls import path

from .views import (
    ScheduleSlotListCreateView,
    ScheduleSlotUpdateDeleteView,
)

urlpatterns = [
    path(
        "",
        ScheduleSlotListCreateView.as_view(),
        name="schedule-list-create",
    ),
    path(
        "<int:pk>/",
        ScheduleSlotUpdateDeleteView.as_view(),
        name="schedule-update-delete",
    ),
]
