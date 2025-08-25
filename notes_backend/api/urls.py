from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import health, register, login_view, logout_view, NoteViewSet

router = DefaultRouter()
router.register(r"notes", NoteViewSet, basename="note")

urlpatterns = [
    path("health/", health, name="Health"),
    path("auth/register/", register, name="Register"),
    path("auth/login/", login_view, name="Login"),
    path("auth/logout/", logout_view, name="Logout"),
    path("", include(router.urls)),
]
