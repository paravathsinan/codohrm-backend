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
        if leave.status == 'Approved':
            return Response({'status': 'Already Approved'})
            
        # If it was previously rejected or pending, we can approve it
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
        old_status = leave.status
        leave.status = 'Rejected'
        leave.save()

        # If it was previously Approved, refund the balance
        if old_status == 'Approved':
            balance = LeaveBalance.objects.filter(
                employee=leave.employee,
                leave_category=leave.leave_category
            ).first()
            if balance:
                balance.used_days -= leave.days
                balance.remaining_days += leave.days
                balance.save()

        return Response({'status': 'Rejected'})

    @action(detail=True, methods=['post'])
    def reset_to_pending(self, request, pk=None):
        leave = self.get_object()
        old_status = leave.status
        leave.status = 'Pending'
        leave.save()

        # If it was previously Approved, refund the balance
        if old_status == 'Approved':
            balance = LeaveBalance.objects.filter(
                employee=leave.employee,
                leave_category=leave.leave_category
            ).first()
            if balance:
                balance.used_days -= leave.days
                balance.remaining_days += leave.days
                balance.save()

        return Response({'status': 'Pending'})

    @action(detail=True, methods=['post'])
    def discuss(self, request, pk=None):
        leave = self.get_object()
        old_status = leave.status
        leave.status = 'Discuss'
        leave.save()

        # If it was previously Approved, refund the balance
        if old_status == 'Approved':
            balance = LeaveBalance.objects.filter(
                employee=leave.employee,
                leave_category=leave.leave_category
            ).first()
            if balance:
                balance.used_days -= leave.days
                balance.remaining_days += leave.days
                balance.save()

        return Response({'status': 'Discuss'})

class LeaveBalanceViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = LeaveBalanceSerializer
    
    def get_queryset(self):
        employee_id = self.request.query_params.get('employee_id')
        
        if employee_id and self.request.user.role in ['admin', 'superadmin']:
            try:
                target_employee = Employee.objects.get(id=employee_id)
            except Employee.DoesNotExist:
                return LeaveBalance.objects.none()
        else:
            try:
                target_employee = Employee.objects.get(user=self.request.user)
            except Employee.DoesNotExist:
                return LeaveBalance.objects.none()

        # Auto-create balances if they don't exist for all categories
        categories = LeaveCategory.objects.all()
        for cat in categories:
            LeaveBalance.objects.get_or_create(
                employee=target_employee,
                leave_category=cat,
                defaults={
                    'total_days': cat.max_days,
                    'remaining_days': cat.max_days
                }
            )
            
        return LeaveBalance.objects.filter(employee=target_employee)
