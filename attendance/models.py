from django.db import models
from core.models import BaseModel
from employees.models import Employee

class AttendanceRecord(BaseModel):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Break', 'Break'),
        ('Clocked Out', 'Clocked Out'),
        ('Late', 'Late'),
        ('Absent', 'Absent'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(blank=True, null=True)
    total_hours = models.CharField(max_length=20, default="0h 0m")
    total_break_seconds = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Present')
    planned_work = models.TextField(blank=True, null=True)
    completed_work = models.TextField(blank=True, null=True)
    
    # Overtime / Extra Hours
    requested_extra_hours = models.FloatField(default=0.0)
    overtime_reason = models.TextField(blank=True, null=True)
    overtime_status = models.CharField(
        max_length=20, 
        choices=(
            ('Pending', 'Pending'),
            ('Approved', 'Approved'),
            ('Rejected', 'Rejected')
        ),
        default='Pending'
    )

    class Meta:
        unique_together = ('employee', 'date')
        ordering = ['-date', '-check_in']

    def __str__(self):
        return f"{self.employee.full_name} - {self.date}"

class AttendanceBreak(BaseModel):
    attendance_record = models.ForeignKey(AttendanceRecord, on_delete=models.CASCADE, related_name='breaks')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    duration_seconds = models.IntegerField(default=0)

    def __str__(self):
        return f"Break for {self.attendance_record}"
