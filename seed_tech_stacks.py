import os
import django
import sys

# Setup django
sys.path.append('c:/Users/parav/OneDrive/Desktop/HRM/codohrm-backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from projects.models import ProjectClassification
from employees.models import Enterprise

def seed_tech_stacks():
    enterprise = Enterprise.objects.first()
    
    stacks = [
        "React", "Next.js", "Node.js", "Python", "Django", 
        "PostgreSQL", "Tailwind CSS", "TypeScript", "AWS S3", 
        "MongoDB", "Flutter", "React Native", "Docker", "Kubernetes"
    ]
    
    for stack_name in stacks:
        obj, created = ProjectClassification.objects.get_or_create(
            name=stack_name,
            defaults={"enterprise": enterprise}
        )
        if created:
            print(f"Added Tech Stack: {stack_name}")
        else:
            print(f"Tech Stack already exists: {stack_name}")

if __name__ == "__main__":
    seed_tech_stacks()
