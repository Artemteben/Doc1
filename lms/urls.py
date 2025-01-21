from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    CourseViewSet,
    LessonListCreateView,
    LessonDetailView,
    SubscriptionAPIView,
)

router = DefaultRouter()
router.register("courses", CourseViewSet, basename="course")

app_name = "lms"

urlpatterns = [
    path("lessons/", LessonListCreateView.as_view(), name="lesson-list"),
    path("lessons/<int:pk>/", LessonDetailView.as_view(), name="lesson-detail"),
    path("", include(router.urls)),
    path("subscriptions/", SubscriptionAPIView.as_view(), name="subscription"),
]
