from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from users.views import CustomTokenObtainPairView

urlpatterns = [
    path('admin/', admin.site.urls),
    # JWT Auth (mapped to frontend expectations)
    path('api/v1/auth/login/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # App URLs
    path('api/v1/employees/', include('employees.urls')),
    path('api/v1/core/', include('core.urls')),
    path('api/v1/attendance/', include('attendance.urls')),
    path('api/v1/leaves/', include('leaves.urls')),
    path('api/v1/projects/', include('projects.urls')),
]
