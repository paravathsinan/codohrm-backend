from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import LeaveRequest, LeaveBalance
from .serializers import LeaveRequestSerializer, LeaveBalanceSerializer
from employees.models import Employee

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
        leave.status = 'Approved'
        leave.save()
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
            return LeaveBalance.objects.filter(employee=employee)
        except Employee.DoesNotExist:
            return LeaveBalance.objects.none()
