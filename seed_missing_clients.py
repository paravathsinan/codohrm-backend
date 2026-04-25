import os
import django
import sys

# Setup django
sys.path.append('c:/Users/parav/OneDrive/Desktop/HRM/codohrm-backend')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from projects.models import Client
from employees.models import Enterprise

def seed_missing_clients():
    # Get the primary enterprise (usually ID 1 or the one with name 'Codo AI')
    enterprise = Enterprise.objects.first()
    
    clients = [
        {
            "company_name": "Albedo Global",
            "name": "Sarah Chen",
            "email": "sarah.chen@albedo.com",
            "website": "https://albedoglobal.com",
            "industry": "Supply Chain",
            "location": "Singapore",
            "status": "Active",
            "notes": "Legacy client migrated from mock data."
        },
        {
            "company_name": "Evoka",
            "name": "Marcus Thorne",
            "email": "marcus@evoka.io",
            "website": "https://evoka.io",
            "industry": "FinTech",
            "location": "London, UK",
            "status": "Active",
            "notes": "Legacy client migrated from mock data."
        }
    ]
    
    for client_data in clients:
        client, created = Client.objects.get_or_create(
            company_name=client_data["company_name"],
            defaults={
                "enterprise": enterprise,
                "name": client_data["name"],
                "email": client_data["email"],
                "website": client_data["website"],
                "industry": client_data["industry"],
                "location": client_data["location"],
                "status": client_data["status"],
                "notes": client_data["notes"]
            }
        )
        if created:
            print(f"Created client: {client.company_name}")
        else:
            print(f"Client already exists: {client.company_name}")

if __name__ == "__main__":
    seed_missing_clients()
