from rest_framework import serializers
from .models import Course, Lesson, Subscription
from .validators import youtube_only_validator


class LessonSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")  # Отображение владельца
    video_url = serializers.URLField(
        validators=[youtube_only_validator]
    )  # Добавлен валидатор

    class Meta:
        model = Lesson
        fields = ["id", "description", "preview", "video_url", "owner"]
        read_only_fields = ["owner"]  # Поле `owner` только для чтения


class CourseSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")  # Отображение владельца
    lesson_count = serializers.SerializerMethodField()  # Подсчет уроков
    lessons = LessonSerializer(
        many=True, read_only=True,
    )  # Правка
    is_subscribed = serializers.SerializerMethodField()  # Проверка подписки

    class Meta:
        model = Course
        fields = ["id", "preview", "description", "lesson_count", "lessons", "owner", "is_subscribed"]
        read_only_fields = ["owner"]  # Поле `owner` только для чтения
        is_subscribed = serializers.SerializerMethodField()

    def get_lesson_count(self, obj):
        return obj.lessons.count()

    def get_is_subscribed(self, obj):
        user = self.context["request"].user
        return Subscription.objects.filter(user=user, course=obj).exists()
