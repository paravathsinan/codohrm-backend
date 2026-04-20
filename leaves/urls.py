from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LeaveViewSet, LeaveBalanceViewSet

router = DefaultRouter()
router.register(r'requests', LeaveViewSet, basename='leave-request')
router.register(r'balances', LeaveBalanceViewSet, basename='leave-balance')

urlpatterns = [
    path('', include(router.urls)),
]
