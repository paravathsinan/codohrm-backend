from django.urls import path
from .views import EmployeeOnboardView

urlpatterns = [
    path('onboard/', EmployeeOnboardView.as_view(), name='employee-onboard'),
]
