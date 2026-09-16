
from django.urls import path

from .views import (
    SessionActionView,
    SessionDetailView,
    SessionListCreateView,
)

urlpatterns = [
    path(
        "",
        SessionListCreateView.as_view(),
        name="session-list-create",
    ),

    path(
        "<int:pk>/",
        SessionDetailView.as_view(),
        name="session-detail",
    ),

    path(
        "<int:pk>/<str:action>/",
        SessionActionView.as_view(),
        name="session-action",
    ),
]
