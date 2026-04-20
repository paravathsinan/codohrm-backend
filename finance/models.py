from django.db import models
from core.models import BaseModel
from employees.models import Employee

class Reimbursement(BaseModel):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Rejected', 'Rejected'),
    )
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='reimbursements')
    transaction_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    purpose = models.CharField(max_length=255)
    supporting_doc_url = models.URLField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')

    def __str__(self):
        return f"{self.employee.full_name} - {self.amount} - {self.status}"
