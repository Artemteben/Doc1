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


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
