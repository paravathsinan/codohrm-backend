from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import LeaveRequest, LeaveBalance, LeaveCategory
from .serializers import LeaveRequestSerializer, LeaveBalanceSerializer, LeaveCategorySerializer
from employees.models import Employee

class LeaveCategoryViewSet(viewsets.ModelViewSet):
    queryset = LeaveCategory.objects.all()
    serializer_class = LeaveCategorySerializer

class LeaveViewSet(viewsets.ModelViewSet):
    serializer_class = LeaveRequestSerializer
    
    def get_queryset(self):
        if self.request.user.role in ['admin', 'superadmin']:
            return LeaveRequest.objects.all().order_by('-created_at')
        try:
            employee = Employee.objects.get(user=self.request.user)
            return LeaveRequest.objects.filter(employee=employee).order_by('-created_at')
        except Employee.DoesNotExist:
            return LeaveRequest.objects.none()
    
    def perform_create(self, serializer):
        employee = get_object_or_404(Employee, user=self.request.user)
        # Calculate days
        start_date = serializer.validated_data['start_date']
        end_date = serializer.validated_data['end_date']
        days = (end_date - start_date).days + 1
        serializer.save(employee=employee, days=days)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        leave = self.get_object()
        if leave.status != 'Approved':
            leave.status = 'Approved'
            leave.save()
            
            # Update Balance
            balance, created = LeaveBalance.objects.get_or_create(
                employee=leave.employee,
                leave_category=leave.leave_category,
                defaults={
                    'total_days': leave.leave_category.max_days,
                    'remaining_days': leave.leave_category.max_days
                }
            )
            balance.used_days += leave.days
            balance.remaining_days -= leave.days
            balance.save()
            
        return Response({'status': 'Approved'})

    @action(detail=True, methods=['post'])
    def reject(self, request, pk=None):
        leave = self.get_object()
        leave.status = 'Rejected'
        leave.save()
        return Response({'status': 'Rejected'})

class LeaveBalanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LeaveBalanceSerializer
    
    def get_queryset(self):
        try:
            employee = Employee.objects.get(user=self.request.user)
            
            # Auto-create balances if they don't exist for all categories
            categories = LeaveCategory.objects.all()
            for cat in categories:
                LeaveBalance.objects.get_or_create(
                    employee=employee,
                    leave_category=cat,
                    defaults={
                        'total_days': cat.max_days,
                        'remaining_days': cat.max_days
                    }
                )
                
            return LeaveBalance.objects.filter(employee=employee)
        except Employee.DoesNotExist:
            return LeaveBalance.objects.none()
