from django.db import models
from core.models import BaseModel
from employees.models import Employee

class LeaveCategory(BaseModel):
    name = models.CharField(max_length=50, unique=True)
    max_days = models.IntegerField(default=12)
    is_paid = models.BooleanField(default=True)
    
    def __str__(self):
        return self.name

class LeaveRequest(BaseModel):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_requests')
    leave_category = models.ForeignKey(LeaveCategory, on_delete=models.SET_NULL, null=True)
    start_date = models.DateField()
    end_date = models.DateField()
    days = models.IntegerField(default=1)
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    
    def __str__(self):
        return f"{self.employee.full_name} - {self.leave_category.name if self.leave_category else 'Unknown'} ({self.start_date})"

class LeaveBalance(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='leave_balances')
    leave_category = models.ForeignKey(LeaveCategory, on_delete=models.CASCADE, null=True, blank=True)
    total_days = models.IntegerField(default=12)
    used_days = models.IntegerField(default=0)
    remaining_days = models.IntegerField(default=12)

    class Meta:
        unique_together = ('employee', 'leave_category')

    def __str__(self):
        return f"{self.employee.full_name} - {self.leave_category.name}: {self.remaining_days} left"
