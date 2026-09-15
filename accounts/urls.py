
from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import (
    LogoutView,
    TherapistAvailabilityView,
    TherapistProfileView,
    TherapistAvatarView,
)

urlpatterns = [
    # Authentication
    path(
        "auth/token/",
        TokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path(
        "auth/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),
    path(
        "auth/logout/",
        LogoutView.as_view(),
        name="logout",
    ),

    # Therapist profile
    path(
        "therapist/profile/",
        TherapistProfileView.as_view(),
        name="therapist-profile",
    ),
    path(
        "therapist/availability/",
        TherapistAvailabilityView.as_view(),
        name="therapist-availability",
    ),
    path( "therapist/avatar/", TherapistAvatarView.as_view(), name="therapist-avatar", ),
]