from rest_framework import serializers
from .models import User
from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = [
            "id",
            "user",
            "course",
            "lesson",
            "payment_date",
            "amount",
            "payment_method",
        ]


class UserSerializer(serializers.ModelSerializer):
    payment_history = PaymentSerializer(many=True)

    class Meta:
        model = User
        fields = ["id", "email", "phone", "city", "avatar", "payment_history"]
