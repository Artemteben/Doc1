from django.urls import path
from rest_framework.routers import SimpleRouter

from lms.apps import LmsConfig
from lms.models import Course, Lesson
from lms.views import (
    CourseViewSet,
    LessonCreateApiView,
    LessonDestroyAPIView,
    LessonListApiView,
    LessonRetrieveAPIView,
    LessonUpdateAPIView,
)

app_name = LmsConfig.name

router = SimpleRouter()

router.register("", CourseViewSet)

urlpatterns = [
    path("lesson/", LessonListApiView.as_view(), name="lesson_list"),
    path("lesson/<int:pk>/", LessonRetrieveAPIView.as_view(), name="lesson_retrieve"),
    path(
        "lesson/<int:pk>/update/", LessonUpdateAPIView.as_view(), name="lesson_update"
    ),
    path(
        "lesson/<int:pk>/delete/", LessonDestroyAPIView.as_view(), name="lesson_destroy"
    ),
    path("lesson/create/", LessonCreateApiView.as_view(), name="lesson_create"),
]
urlpatterns += router.urls
