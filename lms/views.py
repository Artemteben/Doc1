from django.shortcuts import get_object_or_404
from django.utils.timezone import now, timedelta
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    ListCreateAPIView,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Course, Subscription
from .models import Lesson
from .paginators import CustomPagination
from .serializers import CourseSerializer, LessonSerializer
from .tasks import send_course_update_email, notify_subscribers_about_updating_course


class CourseViewSet(viewsets.ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def perform_update(self, serializer):
        course = serializer.save()
        notify_subscribers_about_updating_course.delay(course_id=course.id)


class CourseCreateAPIView(CreateAPIView):
    """
    Создание курсов только для владельцев.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Присваиваем владельца при создании курса
        serializer.save(owner=self.request.user)


class CourseViewSet(viewsets.ModelViewSet):
    """
    CRUD операции для курсов с проверкой прав.
    """

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Модераторы видят все курсы, пользователи — только свои
        if self.request.user.groups.filter(name="Moderator").exists():
            return Course.objects.all()
        return Course.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Запрет на создание курсов для модераторов
        if self.request.user.groups.filter(name="Moderator").exists():
            raise PermissionDenied("Модераторы не могут создавать курсы.")
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        # Запрет на удаление курсов для модераторов
        if self.request.user.groups.filter(name="Moderator").exists():
            raise PermissionDenied("Модераторы не могут удалять курсы.")
        instance.delete()


class LessonViewSet(viewsets.ModelViewSet):
    """
    CRUD операции для уроков с проверкой прав.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Модераторы видят все уроки, пользователи — только свои
        if self.request.user.groups.filter(name="Moderator").exists():
            return Lesson.objects.all()
        return Lesson.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Запрет на создание уроков для модераторов
        if self.request.user.groups.filter(name="Moderator").exists():
            raise PermissionDenied("Модераторы не могут создавать уроки.")
        serializer.save(owner=self.request.user)

    def perform_destroy(self, instance):
        # Запрет на удаление уроков для модераторов
        if self.request.user.groups.filter(name="Moderator").exists():
            raise PermissionDenied("Модераторы не могут удалять уроки.")
        instance.delete()


class LessonListCreateView(ListCreateAPIView):
    """
    Список и создание уроков.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Присваиваем владельца при создании урока
        serializer.save(owner=self.request.user)


class LessonDetailView(RetrieveUpdateDestroyAPIView):
    """
    Детальный просмотр, обновление и удаление урока.
    """

    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]


class SubscriptionAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        course_id = request.data.get("course_id")
        course_item = get_object_or_404(Course, id=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        if subs_item.exists():
            subs_item.delete()
            message = "Подписка удалена"
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = "Подписка добавлена"

        return Response({"message": message})
