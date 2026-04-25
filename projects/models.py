from django.db import models
from core.models import BaseModel
from employees.models import Employee, Enterprise

class Client(BaseModel):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Inactive', 'Inactive'),
        ('Lead', 'Lead'),
    )
    
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='clients', null=True, blank=True)
    company_name = models.CharField(max_length=255)
    website = models.URLField(max_length=255, blank=True, null=True)
    industry = models.CharField(max_length=100, blank=True, null=True)
    gst_id = models.CharField(max_length=50, blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    
    # Primary Contact Info
    name = models.CharField(max_length=255) # Contact person name
    location = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.company_name

class Server(BaseModel):
    STATUS_CHOICES = (
        ('Active', 'Active'),
        ('Maintenance', 'Maintenance'),
        ('Offline', 'Offline'),
        ('Scaling', 'Scaling'),
        ('Decommissioned', 'Decommissioned'),
    )
    
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='servers', null=True, blank=True)
    name = models.CharField(max_length=255)
    type = models.CharField(max_length=50, default='VPS')
    maintained_by = models.CharField(max_length=255, blank=True, null=True)
    root_address = models.CharField(max_length=255, blank=True, null=True)
    password = models.CharField(max_length=255, blank=True, null=True)
    a_record = models.CharField(max_length=255, blank=True, null=True)
    aaaa_record = models.CharField(max_length=255, blank=True, null=True)
    
    # Dates
    purchase_date = models.DateField(null=True, blank=True)
    expiry_date = models.DateField(null=True, blank=True)
    renewal_date = models.DateField(null=True, blank=True)
    alert_date = models.DateField(null=True, blank=True)
    
    provider = models.CharField(max_length=100, blank=True, null=True)
    which_mail = models.CharField(max_length=255, blank=True, null=True)
    mail_password = models.CharField(max_length=255, blank=True, null=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Active')
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Project(BaseModel):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Ongoing', 'Ongoing'),
        ('Completed', 'Completed'),
        ('Maintenance', 'Maintenance'),
    )
    
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='projects', null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    duration = models.IntegerField(default=0) # in days
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Ongoing')
    
    
    project_lead = models.ForeignKey(Employee, on_delete=models.SET_NULL, null=True, blank=True, related_name='led_projects')
    team_members = models.ManyToManyField(Employee, related_name='assigned_projects', blank=True)
    qa_testers = models.ManyToManyField(Employee, related_name='tested_projects', blank=True)
    
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
class ProjectClassification(BaseModel):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='classifications', null=True, blank=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name
