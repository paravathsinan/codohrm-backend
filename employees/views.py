from rest_framework import viewsets, filters, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import (
    Employee, Enterprise, Department, Position, 
    WorkingMode, EmploymentType, SystemRole
)
from .serializers import (
    EmployeeSerializer, EnterpriseSerializer, DepartmentSerializer,
    PositionSerializer, WorkingModeSerializer, 
    EmploymentTypeSerializer, SystemRoleSerializer
)

class EmployeeViewSet(viewsets.ModelViewSet):
    """
    ViewSet for complete Employee CRUD operations.
    """
    def get_queryset(self):
        """
        Exclude superadmins from the general employee directory.
        """
        return Employee.objects.select_related('user', 'address', 'bank_details').prefetch_related('roles').exclude(user__is_superuser=True)

    serializer_class = EmployeeSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    
    # We will need django-filter to make this entirely work, else basic filtering works
    filterset_fields = ['status', 'gender', 'marital_status']
    search_fields = ['full_name', 'phone_number', 'user__email', 'user__username']
    ordering_fields = ['full_name', 'created_at']
    ordering = ['-created_at']

    def perform_destroy(self, instance):
        """
        Ensure the associated User is deleted when the Employee is deleted.
        OneToOneField CASCADE deletes Employee when User is deleted, 
        but we want the reverse here for clean data removal.
        """
        user = instance.user
        instance.delete()
        if user:
            user.delete()

    # Optional: We could restrict permissions so employees only see info that belongs to them or manager
    # but the serializer handles the data logic natively for now.

    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        """
        Return or update the currently logged-in user's employee profile.
        """
        try:
            employee = Employee.objects.select_related('user', 'address', 'bank_details').prefetch_related('roles').get(user=request.user)
            
            if request.method == 'PATCH':
                serializer = self.get_serializer(employee, data=request.data, partial=True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response(serializer.data)
                
            serializer = self.get_serializer(employee)
            return Response(serializer.data)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee profile not found."}, status=status.HTTP_404_NOT_FOUND)

class EnterpriseViewSet(viewsets.ModelViewSet):
    queryset = Enterprise.objects.all()
    serializer_class = EnterpriseSerializer
    permission_classes = [permissions.IsAuthenticated]

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['enterprise']

class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_fields = ['enterprise']

class WorkingModeViewSet(viewsets.ModelViewSet):
    queryset = WorkingMode.objects.all()
    serializer_class = WorkingModeSerializer
    permission_classes = [permissions.IsAuthenticated]

class EmploymentTypeViewSet(viewsets.ModelViewSet):
    queryset = EmploymentType.objects.all()
    serializer_class = EmploymentTypeSerializer
    permission_classes = [permissions.IsAuthenticated]

class SystemRoleViewSet(viewsets.ModelViewSet):
    queryset = SystemRole.objects.all()
    serializer_class = SystemRoleSerializer
    permission_classes = [permissions.IsAuthenticated]
