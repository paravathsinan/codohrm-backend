from django.urls import path
from .views import ActivateAccountView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('activate/', ActivateAccountView.as_view(), name='activate-account'),
]
