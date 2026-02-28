from rest_framework import serializers

from users.models import Payment, User


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "payment_date",
            "course",
            "lesson",
            "amount",
            "method",
        ]


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "phone", "city", "avatar")
        read_only_fields = ("id", "email")


class UserPublicProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "city", "avatar")


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "password",
            "first_name",
            "last_name",
            "phone",
            "city",
            "avatar",
        )
        extra_kwargs = {
            "password": {"write_only": True},
        }
