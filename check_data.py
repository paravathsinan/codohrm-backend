import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from employees.models import Department, Position, Enterprise

print("Enterprises:")
for e in Enterprise.objects.all():
    print(f"ID: {e.id}, Name: {e.name}")

print("\nDepartments:")
for d in Department.objects.all():
    print(f"Name: {d.name}, Enterprise: {d.enterprise.name if d.enterprise else 'None'} (ID: {d.enterprise_id})")

print("\nPositions:")
for p in Position.objects.all():
    print(f"Name: {p.name}, Enterprise: {p.enterprise.name if p.enterprise else 'None'} (ID: {p.enterprise_id})")
