from django.db import models
from core.models import BaseModel
from employees.models import Employee

class LeaveRequest(BaseModel):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    LEAVE_TYPES = (
        ('Sick', 'Sick'),
        ('Casual', 'Casual'),
        ('Earned', 'Earned'),
    )
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    days = models.IntegerField(default=1)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.leave_type} ({self.start_date})"

class LeaveBalance(BaseModel):
    LEAVE_TYPES = (
        ('Sick', 'Sick'),
        ('Casual', 'Casual'),
        ('Earned', 'Earned'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_balances')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    total_days = models.IntegerField(default=12)
    used_days = models.IntegerField(default=0)
    remaining_days = models.IntegerField(default=12)

    class Meta:
        unique_together = ('employee', 'leave_type')

    def __str__(self):
        return f"{self.employee.full_name} - {self.leave_type}: {self.remaining_days} left"
