from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    ROLE_CHOICES = (
        ('superadmin', 'Super Admin'),
        ('hr', 'HR Manager'),
        ('finance', 'Finance Officer'),
        ('manager', 'Department Manager'),
        ('staff', 'Staff'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='staff')

    def save(self, *args, **kwargs):
        if self.is_superuser and self.role == 'staff':
            self.role = 'superadmin'
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"
