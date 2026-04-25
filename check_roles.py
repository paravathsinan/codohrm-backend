import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from employees.models import Employee

print("Checking Employee Roles...")
for emp in Employee.objects.all():
    roles = emp.roles.all()
    print(f"Employee: {emp.full_name}")
    print(f"  Role Count: {roles.count()}")
    for role in roles:
        print(f"    Enterprise: {role.enterprise.name if role.enterprise else 'None'}")
