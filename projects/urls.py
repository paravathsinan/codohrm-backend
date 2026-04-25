from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProjectViewSet, ClientViewSet, ServerViewSet, ProjectClassificationViewSet

router = DefaultRouter()
router.register(r'projects', ProjectViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'servers', ServerViewSet)
router.register(r'classifications', ProjectClassificationViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
