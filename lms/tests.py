from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from .models import Course, Lesson, Subscription

User = get_user_model()


class CourseAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.course = Course.objects.create(owner=self.user, description="Test Course")
        self.lesson = Lesson.objects.create(
            course=self.course, owner=self.user, description="Test Lesson"
        )

    def test_create_course(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/courses/", {"description": "New Course"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_subscription(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/subscriptions/", {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 1)
