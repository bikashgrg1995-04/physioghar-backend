
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path

from config import settings

urlpatterns = [
    path("admin/", admin.site.urls),

    path( "api/v1/", include("accounts.urls"), ),

    path(
        "api/v1/patients/",
        include("patients.urls"),
    ),

    # path(
    #     "api/v1/sessions/",
    #     include("sessions.urls"),
    # ),

    # path(
    #     "api/v1/schedules/",
    #     include("schedules.urls"),
    # ),

    # path(
    #     "api/v1/complaints/",
    #     include("complaints.urls"),
    # ),
]


if settings.DEBUG: 
    urlpatterns += static( 
        settings.MEDIA_URL, 
        document_root=settings.MEDIA_ROOT, 
    )