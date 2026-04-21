from rest_framework import serializers
from .models import AttendanceRecord, AttendanceBreak

class AttendanceBreakSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttendanceBreak
        fields = ('id', 'start_time', 'end_time', 'duration_seconds')

class AttendanceRecordSerializer(serializers.ModelSerializer):
    breaks = AttendanceBreakSerializer(many=True, read_only=True)
    employee_name = serializers.CharField(source='employee.full_name', read_only=True)
    enterprise_name = serializers.ReadOnlyField(source='employee.roles.first.enterprise.name')
    
    class Meta:
        model = AttendanceRecord
        fields = (
            'id', 'employee', 'employee_name', 'enterprise_name', 'date', 'check_in', 'check_out', 
            'total_hours', 'total_break_seconds', 'status', 
            'planned_work', 'completed_work', 'breaks'
        )
        read_only_fields = ('employee',)
