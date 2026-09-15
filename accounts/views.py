
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import TherapistProfile


from .serializers import (
    LogoutSerializer,
    TherapistAvatarSerializer,
    TherapistProfileSerializer,
    TherapistAvailabilitySerializer,

)
from rest_framework.generics import RetrieveUpdateAPIView


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(
            data=request.data,
        )

        serializer.is_valid(
            raise_exception=True,
        )

        serializer.save()

        return Response(
            {
                "detail": "Logout successful.",
            },
            status=status.HTTP_200_OK,
        )

class TherapistProfileView(RetrieveUpdateAPIView): 
    serializer_class = TherapistProfileSerializer 
    permission_classes = [IsAuthenticated] 

    def get_object(self): 
        profile, _ = TherapistProfile.objects.get_or_create( 
            user=self.request.user, 
            ) 

        return profile


class TherapistAvailabilityView(RetrieveUpdateAPIView):
    serializer_class = TherapistAvailabilitySerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, _ = TherapistProfile.objects.get_or_create(
            user=self.request.user,
        )

        return profile

class TherapistAvatarView(RetrieveUpdateAPIView): 
    serializer_class = TherapistAvatarSerializer 
    permission_classes = [IsAuthenticated] 
    parser_classes = [MultiPartParser, FormParser] 

    def get_object(self): 
        profile, _ = TherapistProfile.objects.get_or_create(
            user=self.request.user, 
            ) 

        return profile