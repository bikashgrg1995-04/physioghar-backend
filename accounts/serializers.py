
from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from .models import TherapistProfile


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def save(self, **kwargs):
        refresh_token = self.validated_data["refresh"]

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except Exception as error:
            raise serializers.ValidationError(
                {
                    "detail": "Invalid or already blacklisted refresh token."
                }
            ) from error


class TherapistProfileSerializer(serializers.Serializer):
    name = serializers.CharField()
    email = serializers.EmailField()
    phone = serializers.CharField(allow_blank=True)

    specialization = serializers.CharField(allow_blank=True)
    experience = serializers.CharField(allow_blank=True)
    address = serializers.CharField(allow_blank=True)
    bio = serializers.CharField(allow_blank=True)
    is_available = serializers.BooleanField()

    def to_representation(self, instance):
        return {
            "name": instance.user.get_full_name(),
            "email": instance.user.email,
            "phone": instance.user.phone,
            "specialization": instance.specialization,
            "experience": instance.experience,
            "address": instance.address,
            "bio": instance.bio,
            "is_available": instance.is_available,
        }

    def update(self, instance, validated_data):
        user = instance.user

        name = validated_data.pop("name", None)
        email = validated_data.pop("email", None)
        phone = validated_data.pop("phone", None)

        if name is not None:
            name_parts = name.strip().split()

            user.first_name = name_parts[0] if name_parts else ""
            user.last_name = " ".join(name_parts[1:])

        if email is not None:
            user.email = email.strip().lower()

        if phone is not None:
            user.phone = phone

        user.save(
            update_fields=[
                "first_name",
                "last_name",
                "email",
                "phone",
                "updated_at",
            ]
        )

        for field in [
            "specialization",
            "experience",
            "address",
            "bio",
            "is_available",
        ]:
            if field in validated_data:
                setattr(
                    instance,
                    field,
                    validated_data[field],
                )

        instance.save()

        return instance


class TherapistAvailabilitySerializer(serializers.Serializer):
    is_available = serializers.BooleanField()

    def to_representation(self, instance):
        return {
            "is_available": instance.is_available,
        }

    def update(self, instance, validated_data):
        instance.is_available = validated_data["is_available"]
        instance.save(
            update_fields=[
                "is_available",
                "updated_at",
            ]
        )

        return instance


class TherapistAvatarSerializer(serializers.ModelSerializer): 
    avatar = serializers.ImageField( 
        required=True, 
        ) 

    class Meta: 
        model = TherapistProfile 
        fields = ("avatar",)