import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from projects.models import Client

mock_clients = [
    {
        "name": "John Doe",
        "company_name": "Nexus Digital",
        "email": "john@nexus.co",
        "phone": "+91 9876543210",
        "location": "Bangalore, India",
        "industry": "E-commerce",
        "website": "https://nexus.co",
        "gst_id": "29AAAAA0000A1Z5",
        "status": "Active",
        "notes": "Primary account for digital transformation projects."
    },
    {
        "name": "Sarah Smith",
        "company_name": "Zenith Health",
        "email": "sarah@zenith.health",
        "phone": "+44 20 7946 0958",
        "location": "London, UK",
        "industry": "Healthcare",
        "website": "https://zenith.health",
        "gst_id": "GB123456789",
        "status": "Active",
        "notes": "Healthcare SaaS integration partner."
    }
]

print("Seeding mock clients into database...")
for data in mock_clients:
    client, created = Client.objects.get_or_create(
        company_name=data["company_name"],
        defaults=data
    )
    if created:
        print(f"  Created: {client.company_name}")
    else:
        print(f"  Already exists: {client.company_name}")

print("Seeding complete.")
