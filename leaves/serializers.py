from rest_framework import serializers
from .models import LeaveRequest, LeaveBalance

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.ReadOnlyField(source='employee.full_name')
    
    class Meta:
        model = LeaveRequest
        fields = (
            'id', 'employee', 'employee_name', 'leave_type', 
            'start_date', 'end_date', 'days', 'reason', 'status', 'created_at'
        )
        read_only_fields = ('employee', 'status')

class LeaveBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveBalance
        fields = ('id', 'employee', 'leave_type', 'total_days', 'used_days', 'remaining_days')
        read_only_fields = ('employee',)
