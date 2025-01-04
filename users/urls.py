from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PaymentViewSet, UserViewSet, UserProfileView

router = DefaultRouter()
router.register(r"payments", PaymentViewSet)
router.register(r"users", UserViewSet)

urlpatterns = [
    path("profile/<int:pk>/", UserProfileView.as_view(), name="user-profile"),
    path("", include(router.urls)),
]
