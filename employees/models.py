from django.db import models
from django.conf import settings
from core.models import BaseModel

class Enterprise(BaseModel):
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class Department(BaseModel):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='departments')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('enterprise', 'name')

    def __str__(self):
        return f"{self.enterprise.name} - {self.name}"

class Position(BaseModel):
    enterprise = models.ForeignKey(Enterprise, on_delete=models.CASCADE, related_name='positions')
    name = models.CharField(max_length=100)

    class Meta:
        unique_together = ('enterprise', 'name')

    def __str__(self):
        return f"{self.enterprise.name} - {self.name}"

class WorkingMode(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class EmploymentType(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class SystemRole(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Employee(BaseModel):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('resigned', 'Resigned'),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='employee_profile')
    
    # Basic Details
    full_name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=20)
    photograph_url = models.TextField(blank=True, null=True)
    onboarding_poster_url = models.TextField(blank=True, null=True)
    
    # Detailed Records
    guardian_contact = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=20, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], default='Other')
    marital_status = models.CharField(max_length=20, choices=[('Single', 'Single'), ('Married', 'Married'), ('Divorced', 'Divorced'), ('Widowed', 'Widowed')], default='Single')
    blood_group = models.CharField(max_length=5, blank=True, null=True)
    
    # Links
    portfolio_url = models.TextField(blank=True, null=True)
    linkedin_url = models.TextField(blank=True, null=True)
    github_url = models.TextField(blank=True, null=True)
    whatsapp_number = models.CharField(max_length=20, blank=True, null=True)
    
    # KYC
    aadhaar_number = models.CharField(max_length=20, blank=True, null=True)
    aadhaar_card_url = models.TextField(blank=True, null=True)
    pan_number = models.CharField(max_length=20, blank=True, null=True)
    pan_card_url = models.TextField(blank=True, null=True)
    
    # System Audit
    consent_confirmed = models.BooleanField(default=False)
    onboarding_completed = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    comments = models.TextField(blank=True, null=True)
    resignation_note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.full_name} - {self.user.username}"


class EmployeeAddress(BaseModel):
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='address')
    house_name = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    post_office = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=20)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

class EmployeeBankDetail(BaseModel):
    ACCOUNT_TYPES = (
        ('Savings', 'Savings'),
        ('Current', 'Current'),
    )
    employee = models.OneToOneField(Employee, on_delete=models.CASCADE, related_name='bank_details')
    account_name = models.CharField(max_length=255)
    bank_name = models.CharField(max_length=255)
    account_number = models.CharField(max_length=50)
    ifsc = models.CharField(max_length=20)
    branch_name = models.CharField(max_length=100)
    account_type = models.CharField(max_length=20, choices=ACCOUNT_TYPES, default='Savings')
    upi_id = models.CharField(max_length=100, blank=True, null=True)
    upi_phone_number = models.CharField(max_length=20, blank=True, null=True)

class EmployeeRole(BaseModel):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='roles')
    enterprise = models.ForeignKey(Enterprise, on_delete=models.SET_NULL, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    position = models.ForeignKey(Position, on_delete=models.SET_NULL, null=True, blank=True)
    reported_to = models.CharField(max_length=100, blank=True, null=True)
    working_mode = models.ForeignKey(WorkingMode, on_delete=models.SET_NULL, null=True, blank=True)
    employment_type = models.ForeignKey(EmploymentType, on_delete=models.SET_NULL, null=True, blank=True)
    working_hour = models.IntegerField(default=8)
    work_days = models.IntegerField(default=5)
    hourly_payment = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    joining_date = models.DateField(blank=True, null=True)
