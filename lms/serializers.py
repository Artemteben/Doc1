from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Уроков.
    """

    class Meta:
        model = Lesson
        fields = ["id", "description", "preview", "video_url"]


class CourseSerializer(serializers.ModelSerializer):
    """
    Сериализатор для модели Курс.
    """

    lesson_count = serializers.SerializerMethodField()
    lessons = LessonSerializer(many=True)

    class Meta:
        model = Course
        fields = ["id", "preview", "description", "lesson_count", "lessons"]

    def get_lesson_count(self, obj):
        return obj.lessons.count()
