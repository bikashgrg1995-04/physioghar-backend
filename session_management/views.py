
from django.db import transaction
from rest_framework import generics, serializers, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from schedules.models import ScheduleSlot

from .models import Session, SessionStatus
from .serializers import SessionSerializer


class SessionListCreateView(
    generics.ListCreateAPIView,
):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = (
            Session.objects
            .filter(
                therapist=self.request.user,
            )
            .select_related(
                "patient",
                "schedule_slot",
            )
        )

        # Filter by session status.
        session_status = self.request.query_params.get(
            "status",
        )

        if session_status:
            queryset = queryset.filter(
                status=session_status,
            )

        # Filter by patient. 
        patient_id = self.request.query_params.get( 
            "patient", 
        ) 

        if patient_id: 
            queryset = queryset.filter( 
                patient_id=patient_id, 
            )

        return queryset

    @transaction.atomic
    def perform_create(self, serializer):
        schedule_slot = serializer.validated_data[
            "schedule_slot"
        ]

        schedule_slot = (
            ScheduleSlot.objects
            .select_for_update()
            .get(pk=schedule_slot.pk)
        )

        if schedule_slot.therapist_id != self.request.user.id:
            raise serializers.ValidationError(
                {
                    "schedule_slot": (
                        "You can only use your own "
                        "schedule slots."
                    )
                }
            )

        if schedule_slot.status != "open":
            raise serializers.ValidationError(
                {
                    "schedule_slot": (
                        "Only open schedule slots "
                        "can be booked."
                    )
                }
            )

        active_session_exists = Session.objects.filter(
            schedule_slot=schedule_slot,
            status__in=[
                SessionStatus.REQUESTED,
                SessionStatus.UPCOMING,
            ],
        ).exists()

        if active_session_exists:
            raise serializers.ValidationError(
                {
                    "schedule_slot": (
                        "This schedule slot already "
                        "has an active session."
                    )
                }
            )

        serializer.save(
            therapist=self.request.user,
            status=SessionStatus.REQUESTED,
        )

        schedule_slot.status = (
            "booked"
        )

        schedule_slot.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )


class SessionDetailView(
    generics.RetrieveAPIView,
):
    serializer_class = SessionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            Session.objects
            .filter(
                therapist=self.request.user,
            )
            .select_related(
                "patient",
                "schedule_slot",
            )
        )


class SessionActionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(
        self,
        request,
        pk,
        action,
    ):
        if action not in {
            "accept",
            "decline",
            "reschedule",
            "complete",
            "cancel",
        }:
            return Response(
                {
                    "detail": (
                        "Unsupported session action."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        session = (
            Session.objects
            .select_related(
                "patient",
                "schedule_slot",
            )
            .filter(
                pk=pk,
                therapist=request.user,
            )
            .first()
        )

        if session is None:
            return Response(
                {
                    "detail": "Session not found."
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if action == "accept":
            return self._accept(
                request,
                session,
            )

        if action == "decline":
            return self._decline(
                request,
                session,
            )

        if action == "reschedule":
            return self._reschedule(
                request,
                session,
            )

        if action == "complete":
            return self._complete(
                request,
                session,
            )

        return self._cancel(
            request,
            session,
        )

    def _accept(
        self,
        request,
        session,
    ):
        if session.status != SessionStatus.REQUESTED:
            return Response(
                {
                    "detail": (
                        "Only requested sessions "
                        "can be accepted."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        session.status = SessionStatus.UPCOMING

        session.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return self._success_response(
            request,
            session,
        )

    @transaction.atomic
    def _decline(
        self,
        request,
        session,
    ):
        if session.status != SessionStatus.REQUESTED:
            return Response(
                {
                    "detail": (
                        "Only requested sessions "
                        "can be declined."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        reason = (
            request.data.get(
                "cancellation_reason",
            )
            or ""
        ).strip()

        if not reason:
            return Response(
                {
                    "cancellation_reason": (
                        "Cancellation reason is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        schedule_slot = (
            ScheduleSlot.objects
            .select_for_update()
            .get(
                pk=session.schedule_slot_id,
            )
        )

        session.status = SessionStatus.CANCELLED
        session.cancellation_reason = reason

        session.save(
            update_fields=[
                "status",
                "cancellation_reason",
                "updated_at",
            ],
        )

        schedule_slot.status = (
            "open"
        )

        schedule_slot.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return self._success_response(
            request,
            session,
        )

    @transaction.atomic
    def _reschedule(
        self,
        request,
        session,
    ):
        if session.status != SessionStatus.UPCOMING:
            return Response(
                {
                    "detail": (
                        "Only upcoming sessions "
                        "can be rescheduled."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_slot_id = request.data.get(
            "schedule_slot",
        )

        if not new_slot_id:
            return Response(
                {
                    "schedule_slot": (
                        "A new schedule slot is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if str(new_slot_id) == str(
            session.schedule_slot_id,
        ):
            return Response(
                {
                    "schedule_slot": (
                        "Please select a different "
                        "schedule slot."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        new_slot = (
            ScheduleSlot.objects
            .select_for_update()
            .filter(
                pk=new_slot_id,
                therapist=request.user,
            )
            .first()
        )

        if new_slot is None:
            return Response(
                {
                    "schedule_slot": (
                        "Schedule slot not found."
                    )
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        if new_slot.status != "open":
            return Response(
                {
                    "schedule_slot": (
                        "Only open schedule slots "
                        "can be selected."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        active_session_exists = Session.objects.filter(
            schedule_slot=new_slot,
            status__in=[
                SessionStatus.REQUESTED,
                SessionStatus.UPCOMING,
            ],
        ).exclude(
            pk=session.pk,
        ).exists()

        if active_session_exists:
            return Response(
                {
                    "schedule_slot": (
                        "This schedule slot already "
                        "has an active session."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        old_slot = (
            ScheduleSlot.objects
            .select_for_update()
            .get(
                pk=session.schedule_slot_id,
            )
        )

        session.schedule_slot = new_slot

        session.save(
            update_fields=[
                "schedule_slot",
                "updated_at",
            ],
        )

        old_slot.status = "open"

        old_slot.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        new_slot.status = "booked"

        new_slot.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return self._success_response(
            request,
            session,
        )

    @transaction.atomic
    def _complete(
        self,
        request,
        session,
    ):
        if session.status != SessionStatus.UPCOMING:
            return Response(
                {
                    "detail": (
                        "Only upcoming sessions "
                        "can be completed."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        notes = (
            request.data.get(
                "notes",
            )
            or ""
        ).strip()

        if not notes:
            return Response(
                {
                    "notes": (
                        "Completion notes are required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        session.status = SessionStatus.COMPLETED
        session.notes = notes

        session.save(
            update_fields=[
                "status",
                "notes",
                "updated_at",
            ],
        )

        return self._success_response(
            request,
            session,
        )

    @transaction.atomic
    def _cancel(
        self,
        request,
        session,
    ):
        if session.status not in (
            SessionStatus.REQUESTED,
            SessionStatus.UPCOMING,
        ):
            return Response(
                {
                    "detail": (
                        "Only requested or upcoming "
                        "sessions can be cancelled."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        reason = (
            request.data.get(
                "cancellation_reason",
            )
            or ""
        ).strip()

        if not reason:
            return Response(
                {
                    "cancellation_reason": (
                        "Cancellation reason is required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        schedule_slot = (
            ScheduleSlot.objects
            .select_for_update()
            .get(
                pk=session.schedule_slot_id,
            )
        )

        session.status = SessionStatus.CANCELLED
        session.cancellation_reason = reason

        session.save(
            update_fields=[
                "status",
                "cancellation_reason",
                "updated_at",
            ],
        )

        schedule_slot.status = "open"

        schedule_slot.save(
            update_fields=[
                "status",
                "updated_at",
            ],
        )

        return self._success_response(
            request,
            session,
        )

    def _success_response(
        self,
        request,
        session,
    ):
        serializer = SessionSerializer(
            session,
            context={
                "request": request,
            },
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
