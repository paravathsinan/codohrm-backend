from django.db import models
from core.models import BaseModel
from employees.models import Employee, Enterprise

class AttendanceRecord(BaseModel):
    STATUS_CHOICES = (
        ('Present', 'Present'),
        ('Break', 'Break'),
        ('Clocked Out', 'Clocked Out'),
        ('Late', 'Late'),
        ('Absent', 'Absent'),
    )
    REPORT_STATUS_CHOICES = (
        ('In Progress', 'In Progress'),
        ('Completed', 'Completed'),
        ('Delayed', 'Delayed'),
        ('On Hold', 'On Hold'),
    )
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='attendance', null=True, blank=True)
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='attendance')
    date = models.DateField()
    check_in = models.DateTimeField()
    check_out = models.DateTimeField(blank=True, null=True)
    total_hours = models.CharField(max_length=20, default="0h 0m")
    total_break_seconds = models.IntegerField(default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Present')
    planned_work = models.TextField(blank=True, null=True)
    projects = models.ManyToManyField('projects.Project', related_name='attendance_records', blank=True)
    completed_work = models.TextField(blank=True, null=True)
    report_status = models.CharField(max_length=20, choices=REPORT_STATUS_CHOICES, default='In Progress')
    
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
        unique_together = ('employee', 'date', 'enterprise')
        ordering = ['-date', '-check_in']

    def save(self, *args, **kwargs):
        # Auto-complete report status on check-out if it's still "In Progress"
        if self.check_out and self.report_status == 'In Progress':
            self.report_status = 'Completed'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.full_name} - {self.date}"

class AttendanceBreak(BaseModel):
    attendance_record = models.ForeignKey(AttendanceRecord, on_delete=models.CASCADE, related_name='breaks')
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(blank=True, null=True)
    duration_seconds = models.IntegerField(default=0)

    def __str__(self):
        return f"Break for {self.attendance_record}"
