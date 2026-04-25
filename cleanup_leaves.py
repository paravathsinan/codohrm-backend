import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from leaves.models import LeaveBalance
from django.db.models import Count

print("Identifying duplicates...")
duplicates = LeaveBalance.objects.values('employee', 'leave_category', 'enterprise').annotate(count=Count('id')).filter(count__gt=1)

for dup in duplicates:
    print(f"Duplicate found: {dup}")
    lbs = LeaveBalance.objects.filter(
        employee=dup['employee'], 
        leave_category=dup['leave_category'], 
        enterprise=dup['enterprise']
    ).order_by('id')
    
    # Keep the first one, delete the rest
    to_delete = lbs[1:]
    print(f"  Deleting {len(to_delete)} duplicate records...")
    for lb in to_delete:
        lb.delete()

print("Cleanup complete.")
