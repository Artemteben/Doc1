from rest_framework.generics import RetrieveUpdateAPIView
from .models import User
from .serializers import UserSerializer
import django_filters
from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer
from lms.models import Course, Lesson


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
    filterset_class = PaymentFilter  # фильтрация
    ordering_fields = ["payment_date"]  # сортировка
    ordering = ["-payment_date"]  # Сортировка по дате по умолчанию


class UserProfileView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
