from rest_framework import serializers
from .models import LeaveRequest, LeaveBalance, LeaveCategory

class LeaveCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = LeaveCategory
        fields = ('id', 'name', 'max_days', 'is_paid')

class LeaveRequestSerializer(serializers.ModelSerializer):
    employee_name = serializers.ReadOnlyField(source='employee.full_name')
    employee_position = serializers.SerializerMethodField()
    category_name = serializers.ReadOnlyField(source='leave_category.name')

    def get_employee_position(self, obj):
        role = obj.employee.roles.first()
        if role and role.position:
            return role.position.name
        return "—"
    
    class Meta:
        model = LeaveRequest
        fields = (
            'id', 'employee', 'employee_name', 'employee_position', 'leave_category', 
            'category_name', 'start_date', 'end_date', 'days', 'reason', 'status', 'created_at'
        )
        read_only_fields = ('employee', 'status')

class LeaveBalanceSerializer(serializers.ModelSerializer):
    leave_type = serializers.ReadOnlyField(source='leave_category.name')
    category_name = serializers.ReadOnlyField(source='leave_category.name')
    is_paid = serializers.ReadOnlyField(source='leave_category.is_paid')

    class Meta:
        model = LeaveBalance
        fields = ('id', 'employee', 'leave_category', 'leave_type', 'category_name', 'is_paid', 'total_days', 'used_days', 'remaining_days')
        read_only_fields = ('employee',)
