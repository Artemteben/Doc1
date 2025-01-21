from rest_framework.generics import RetrieveUpdateAPIView
from .models import User
from .serializers import UserSerializer, TokenSerializer
import django_filters
from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer, RegisterSerializer
from lms.models import Course, Lesson
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import (
    create_stripe_product,
    create_stripe_price,
    create_stripe_checkout_session,
)
from .models import Payment
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.response import Response
from django.utils.timezone import now


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        user = self.user
        if user:
            user.last_login = now()
            user.save()
        return response


class StripePaymentView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        lesson_id = request.data.get("lesson_id")
        amount = request.data.get("amount")

        if not amount or (not course_id and not lesson_id):
            return Response(
                {"error": "Необходимы данные о курсе или уроке и сумма"}, status=400
            )

        # Создаём продукт и цену в Stripe
        product_name = f"Курс {course_id}" if course_id else f"Урок {lesson_id}"
        product_id = create_stripe_product(product_name)
        price_id = create_stripe_price(product_id, amount)

        # Создаём сессию оплаты
        success_url = "http://localhost:8000/success/"
        cancel_url = "http://localhost:8000/cancel/"
        session_id, session_url = create_stripe_checkout_session(
            price_id, success_url, cancel_url
        )

        # Сохраняем платёж в базе данных
        payment = Payment.objects.create(
            user=user,
            course_id=course_id,
            lesson_id=lesson_id,
            amount=amount,
            stripe_session_id=session_id,
        )

        return Response({"payment_id": payment.id, "stripe_url": session_url})


class PaymentFilter(django_filters.FilterSet):
    date = django_filters.DateTimeFilter(field_name="payment_date", lookup_expr="gte")
    course = django_filters.ModelChoiceFilter(queryset=Course.objects.all())
    lesson = django_filters.ModelChoiceFilter(queryset=Lesson.objects.all())
    payment_method = django_filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)

    class Meta:
        model = Payment
        fields = ["payment_date", "course", "lesson", "payment_method"]


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_class = PaymentFilter  # Применение фильтрации
    ordering_fields = ["payment_date"]  # Возможность сортировки
    ordering = ["-payment_date"]  # Сортировка по дате по умолчанию


class UserProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]


class RegisterView(viewsets.ViewSet):
    def create(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({"user": UserSerializer(user).data}, status=201)
        return Response(serializer.errors, status=400)


class TokenView(TokenObtainPairView):
    serializer_class = TokenSerializer
