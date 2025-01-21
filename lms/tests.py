from django.test import TestCase
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


class LessonViewSetAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.moderator = User.objects.create_user(
            username="moderator", password="password"
        )
        self.moderator.groups.create(name="Moderator")
        self.course = Course.objects.create(owner=self.user, description="Test Course")
        self.lesson = Lesson.objects.create(
            course=self.course, owner=self.user, title="Test Lesson"
        )

    def test_moderator_cannot_create_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.post(
            "/lessons/", {"title": "New Lesson", "course": self.course.id}
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_create_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/lessons/", {"title": "New Lesson", "course": self.course.id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 2)

    def test_moderator_cannot_delete_lesson(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.delete(f"/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_user_can_delete_own_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)

    def test_moderator_can_view_all_lessons(self):
        self.client.force_authenticate(user=self.moderator)
        response = self.client.get("/lessons/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_user_can_view_only_own_lessons(self):
        other_user = User.objects.create_user(username="otheruser", password="password")
        Lesson.objects.create(
            course=self.course, owner=other_user, title="Other Lesson"
        )
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/lessons/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class LessonListCreateViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.course = Course.objects.create(owner=self.user, description="Test Course")

    def test_create_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post(
            "/lessons/", {"title": "New Lesson", "course": self.course.id}
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.count(), 1)

    def test_view_lessons(self):
        Lesson.objects.create(course=self.course, owner=self.user, title="Test Lesson")
        self.client.force_authenticate(user=self.user)
        response = self.client.get("/lessons/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class LessonDetailViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.lesson = Lesson.objects.create(owner=self.user, title="Test Lesson")

    def test_update_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.patch(
            f"/lessons/{self.lesson.id}/", {"title": "Updated Lesson"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.lesson.refresh_from_db()
        self.assertEqual(self.lesson.title, "Updated Lesson")

    def test_delete_lesson(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(f"/lessons/{self.lesson.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.count(), 0)


class SubscriptionAPIViewTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password")
        self.course = Course.objects.create(owner=self.user, description="Test Course")

    def test_add_subscription(self):
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/subscriptions/", {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 1)
        self.assertEqual(response.data["message"], "Подписка добавлена")

    def test_remove_subscription(self):
        Subscription.objects.create(user=self.user, course=self.course)
        self.client.force_authenticate(user=self.user)
        response = self.client.post("/subscriptions/", {"course_id": self.course.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Subscription.objects.count(), 0)
        self.assertEqual(response.data["message"], "Подписка удалена")


# Create your tests here.
