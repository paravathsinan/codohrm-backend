from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EmployeeViewSet, EnterpriseViewSet, DepartmentViewSet, 
    PositionViewSet, WorkingModeViewSet, EmploymentTypeViewSet, SystemRoleViewSet
)

router = DefaultRouter()
router.register(r'enterprises', EnterpriseViewSet, basename='enterprise')
router.register(r'departments', DepartmentViewSet, basename='department')
router.register(r'positions', PositionViewSet, basename='position')
router.register(r'working-modes', WorkingModeViewSet, basename='working-mode')
router.register(r'employment-types', EmploymentTypeViewSet, basename='employment-type')
router.register(r'system-roles', SystemRoleViewSet, basename='system-role')
router.register(r'', EmployeeViewSet, basename='employee')

urlpatterns = [
    path('', include(router.urls)),
]
