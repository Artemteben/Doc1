from django.db import models


class Course(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название курса")
    preview = models.ImageField(
        upload_to="course_previews/",
        verbose_name="превью (картинка)",
        help_text="Загрузите картинку",
        null=True,
        blank=True,
    )
    description = models.TextField(verbose_name="Описание курса", null=True, blank=True)

    class Meta:
        verbose_name = "Курс"
        verbose_name_plural = "Курсы"


class Lesson(models.Model):
    title = models.CharField(max_length=100, verbose_name="Название урока")
    course = models.ForeignKey(Course, verbose_name="Курс", on_delete=models.CASCADE)
    description = models.TextField(verbose_name="Описание урока", null=True, blank=True)
    preview = models.ImageField(
        upload_to="lesson_previews/",
        verbose_name="превью (картинка)",
        help_text="Загрузите картинку",
        null=True,
        blank=True,
    )
    video_url = models.URLField(
        verbose_name="Ссылка на видео",
        help_text="Вставьте ссылку на видео",
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"
