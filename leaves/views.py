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
        if self.request.user.role == 'admin':
            return LeaveRequest.objects.all().order_by('-created_at')
        try:
            employee = Employee.objects.get(user=self.request.user)
            return LeaveRequest.objects.filter(employee=employee).order_by('-created_at')
        except Employee.DoesNotExist:
            return LeaveRequest.objects.none()
    
    def perform_create(self, serializer):
        employee = get_object_or_404(Employee, user=self.request.user)
        serializer.save(employee=employee)

class LeaveBalanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LeaveBalanceSerializer
    
    def get_queryset(self):
        try:
            employee = Employee.objects.get(user=self.request.user)
            return LeaveBalance.objects.filter(employee=employee)
        except Employee.DoesNotExist:
            return LeaveBalance.objects.none()
