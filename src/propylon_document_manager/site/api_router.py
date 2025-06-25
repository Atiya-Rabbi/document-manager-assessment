from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter

from propylon_document_manager.file_versions.api.views import FileVersionViewSet, RegisterViewSet, LoginViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("file_versions", FileVersionViewSet)
router.register("register", RegisterViewSet, basename="register")
router.register("login", LoginViewSet, basename="login")


app_name = "api"
urlpatterns = router.urls
