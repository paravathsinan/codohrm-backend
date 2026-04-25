import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()
from projects.models import Server

default_servers = [
    {
        "name": "Main Production Cluster", 
        "type": "Cloud",
        "maintained_by": "Lead Engineer",
        "root_address": "84.21.12.100", 
        "password": "••••••••••••",
        "a_record": "api.codo.ai",
        "aaaa_record": "2001:0db8:85a3:0000:0000:8a2e:0370:7334",
        "purchase_date": "2024-01-10",
        "expiry_date": "2025-01-10",
        "renewal_date": "2025-01-05",
        "alert_date": "2024-12-25",
        "provider": "AWS",
        "which_mail": "admin@codo.ai",
        "mail_password": "••••••••••••",
        "status": "Active",
        "notes": "Primary production environment for core services."
    }
]

print("Seeding infrastructure nodes into database...")
for data in default_servers:
    server, created = Server.objects.get_or_create(
        name=data["name"],
        defaults=data
    )
    if created:
        print(f"  Deployed: {server.name}")
    else:
        print(f"  Node already online: {server.name}")

print("Infrastructure seeding complete.")
