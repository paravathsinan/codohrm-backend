from django.db import models
from django.conf import settings

class Employee(models.Model):
    """
    Employee model for storing personal and professional details.
    Linked to the custom User model.
    """
    STATUS_CHOICES = [
        ('onboarding', 'Onboarding'),
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    # Link to custom user model
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='employee_profile'
    )
    
    employee_id = models.CharField(max_length=20, unique=True)

    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    department = models.CharField(max_length=100)
    designation = models.CharField(max_length=100)

    joining_date = models.DateField()
    salary = models.DecimalField(max_digits=10, decimal_places=2)

    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='onboarding'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.employee_id})"
