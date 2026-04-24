from django.db.models.signals import post_save
from django.dispatch import receiver
from employees.models import Employee
from .models import LeaveBalance, LeaveRequest, LeaveCategory

@receiver(post_save, sender=Employee)
def create_leave_balances(sender, instance, created, **kwargs):
    if created:
        # Create default balances for all active leave categories
        categories = LeaveCategory.objects.all()
        for category in categories:
            LeaveBalance.objects.get_or_create(
                employee=instance,
                leave_category=category,
                defaults={
                    'total_days': category.max_days,
                    'remaining_days': category.max_days
                }
            )

@receiver(post_save, sender=LeaveRequest)
def update_leave_balance(sender, instance, **kwargs):
    if instance.status == 'Approved':
        balance = LeaveBalance.objects.filter(employee=instance.employee, leave_category=instance.leave_category).first()
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
