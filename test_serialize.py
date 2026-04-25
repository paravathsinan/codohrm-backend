import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from employees.models import Employee
from employees.serializers import EmployeeSerializer

emp = Employee.objects.get(full_name="CODO Super Admin")
serializer = EmployeeSerializer(emp)
try:
    print(serializer.data)
except Exception as e:
    print(f"Serialization failed: {e}")
    import traceback
    traceback.print_exc()
