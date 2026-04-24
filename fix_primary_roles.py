import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from employees.models import Employee

def fix_primary_roles():
    employees = Employee.objects.all()
    count = 0
    for emp in employees:
        roles = emp.roles.all().order_by('created_at')
        if roles.exists():
            # Check if any role is already primary
            if not roles.filter(is_primary=True).exists():
                primary_role = roles.first()
                primary_role.is_primary = True
                primary_role.save()
                count += 1
                print(f"Set primary role for {emp.full_name}")
    print(f"Updated {count} employees.")

if __name__ == "__main__":
    fix_primary_roles()
