import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from employees.models import Employee
from django.contrib.auth import get_user_model

User = get_user_model()

print("Checking Employees...")
for emp in Employee.objects.all():
    print(f"Employee: {emp.full_name}, User: {emp.user.username}")
    try:
        addr = emp.address
        print(f"  Address: {addr.city}")
    except Exception as e:
        print(f"  Address Error: {e}")
        
    try:
        bank = emp.bank_details
        print(f"  Bank: {bank.bank_name}")
    except Exception as e:
        print(f"  Bank Error: {e}")

print("\nChecking Users without Employees...")
for user in User.objects.all():
    if not hasattr(user, 'employee_profile'):
        print(f"User {user.username} (Superuser: {user.is_superuser}) has no employee profile.")
