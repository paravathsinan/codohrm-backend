from django.db import models
from core.models import BaseModel
from employees.models import Employee

class EmployeeTask(BaseModel):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Upcoming', 'Upcoming'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='tasks')
    title = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    notes = models.TextField(blank=True, null=True)
    date = models.DateField()

    def __str__(self):
        return f"{self.title} - {self.status}"

class PerformanceSnapshot(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='performance_snapshots')
    period = models.CharField(max_length=50) # Weekly / Monthly
    date = models.DateField()
    rating = models.IntegerField() # 1-5
    feedback = models.TextField()

    def __str__(self):
        return f"{self.employee.full_name} - {self.period} - {self.rating}"

class KeyPerformanceScore(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='kps')
    metric = models.CharField(max_length=255)
    score = models.IntegerField() # 0-100
    target = models.IntegerField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.metric}: {self.score}/{self.target}"

class KeyResultIndicator(BaseModel):
    STATUS_CHOICES = (
        ('Critical', 'Critical'),
        ('Warning', 'Warning'),
        ('Healthy', 'Healthy'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='kri')
    indicator = models.CharField(max_length=255)
    value = models.CharField(max_length=100)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Healthy')

    def __str__(self):
        return f"{self.indicator} - {self.status}"
