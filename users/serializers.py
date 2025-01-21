from rest_framework import serializers
from rest_framework_simplejwt import settings

from .models import User
from rest_framework import serializers
from .models import Payment
import stripe
from django.conf import settings

stripe.api_key = settings.STRIPE_SECRET_KEY


def create_stripe_product(name):
    """Создать продукт в Stripe"""
    product = stripe.Product.create(name=name)
    return product['id']


def create_stripe_price(product_id, amount):
    """Создать цену для продукта в Stripe"""
    price = stripe.Price.create(unit_amount=int(amount * 100),  # цена в копейках
                                currency="usd", product=product_id, )
    return price['id']


def create_stripe_checkout_session(price_id, success_url, cancel_url):
    """Создать сессию оплаты в Stripe"""
    session = stripe.checkout.Session.create(payment_method_types=["card"],
                                             line_items=[{"price": price_id, "quantity": 1}], mode="payment",
                                             success_url=success_url,
                                             cancel_url=cancel_url, )
    return session['id'], session['url']


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
        fields = ["username", "email", "password"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user


class TokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()
    access = serializers.CharField()
