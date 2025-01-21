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
        many=True, required=False
    )  # Включение уроков в сериализатор курса

    class Meta:
        model = Course
        fields = ["id", "preview", "description", "lesson_count", "lessons", "owner"]
        read_only_fields = ["owner"]  # Поле `owner` только для чтения
        is_subscribed = serializers.SerializerMethodField()

        def get_lesson_count(self, obj):
            return obj.lessons.count()

        def get_is_subscribed(self, obj):
            user = self.context["request"].user
            return Subscription.objects.filter(user=user, course=obj).exists()

    def get_lesson_count(self, obj):
        # Подсчет количества уроков для курса
        return obj.lessons.count()

    def create(self, validated_data):
        # Создание курса с привязкой к урокам
        lessons_data = validated_data.pop("lessons", [])
        course = Course.objects.create(**validated_data)
        for lesson_data in lessons_data:
            Lesson.objects.create(
                course=course, **lesson_data, owner=self.context["request"].user
            )
        return course

    def update(self, instance, validated_data):
        # Обновление курса с учетом уроков
        lessons_data = validated_data.pop("lessons", [])
        instance.description = validated_data.get("description", instance.description)
        instance.preview = validated_data.get("preview", instance.preview)
        instance.save()

        # Обновление или создание связанных уроков
        for lesson_data in lessons_data:
            lesson_id = lesson_data.get("id", None)
            if lesson_id:
                lesson = Lesson.objects.filter(id=lesson_id, course=instance).first()
                if lesson:
                    for attr, value in lesson_data.items():
                        setattr(lesson, attr, value)
                    lesson.save()
            else:
                Lesson.objects.create(
                    course=instance, **lesson_data, owner=self.context["request"].user
                )
        return instance
