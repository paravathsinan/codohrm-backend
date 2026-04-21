from django.db import models
from core.models import BaseModel
from employees.models import Employee

class Project(BaseModel):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Maintenance', 'Maintenance'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration = models.IntegerField(default=0) # in days
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Ongoing')
    
    
    project_lead = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_projects')
    team_members = models.ManyToManyField(Employee, related_name='assigned_projects', blank=True)
    
    # Infrastructure & Links (Stored as JSON for flexibility)
    infrastructure = models.JSONField(default=dict, blank=True)
    links = models.JSONField(default=list, blank=True)
    documents = models.JSONField(default=list, blank=True)
    
    # Tech Stack
    stack = models.JSONField(default=list, blank=True)
    additions = models.JSONField(default=list, blank=True)
    
    # Timeline
    expected_publish = models.DateField(null=True, blank=True)
    testing_date = models.DateField(null=True, blank=True)
    frontend_finish_date = models.DateField(null=True, blank=True)
    backend_finish_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.title
