from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .models import User
from .serializers import UserSerializer, TokenSerializer
import django_filters
from rest_framework import viewsets
from .models import Payment
from .serializers import PaymentSerializer, RegisterSerializer
from lms.models import Course, Lesson
from rest_framework.permissions import IsAuthenticated


class PaymentFilter(django_filters.FilterSet):
    date = django_filters.DateTimeFilter(field_name="payment_date", lookup_expr='gte')
    course = django_filters.ModelChoiceFilter(queryset=Course.objects.all())
    lesson = django_filters.ModelChoiceFilter(queryset=Lesson.objects.all())
    payment_method = django_filters.ChoiceFilter(choices=Payment.PAYMENT_METHOD_CHOICES)

    class Meta:
        model = Payment
        fields = ['payment_date', 'course', 'lesson', 'payment_method']


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filterset_class = PaymentFilter  # Применение фильтрации
    ordering_fields = ['payment_date']  # Возможность сортировки
    ordering = ['-payment_date']  # Сортировка по дате по умолчанию


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
            return Response({
                "user": UserSerializer(user).data
            }, status=201)
        return Response(serializer.errors, status=400)


class TokenView(TokenObtainPairView):
    serializer_class = TokenSerializer
