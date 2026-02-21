from rest_framework import serializers

from users.models import Payment


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
