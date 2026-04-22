from django.db.models.signals import post_save
from django.dispatch import receiver
from employees.models import Employee
from .models import LeaveBalance, LeaveRequest

@receiver(post_save, sender=Employee)
def create_leave_balances(sender, instance, created, **kwargs):
    if created:
        LeaveBalance.objects.create(employee=instance, leave_type='Sick', total_days=10, remaining_days=10)
        LeaveBalance.objects.create(employee=instance, leave_type='Casual', total_days=15, remaining_days=15)
        LeaveBalance.objects.create(employee=instance, leave_type='Earned', total_days=15, remaining_days=15)

@receiver(post_save, sender=LeaveRequest)
def update_leave_balance(sender, instance, **kwargs):
    if instance.status == 'Approved':
        balance = LeaveBalance.objects.filter(employee=instance.employee, leave_type=instance.leave_type).first()
        if balance:
            # Check if this request was already deducted to prevent double-deduction
            # For simplicity in this HRM, we assume status changes to Approved only once.
            # In a production app, we would track if 'is_deducted' or similar.
            
            # Calculate days if it's not set correctly
            if not instance.days:
                delta = instance.end_date - instance.start_date
                instance.days = delta.days + 1
            
            balance.used_days += instance.days
            balance.remaining_days = max(0, balance.total_days - balance.used_days)
            balance.save()
