from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model

from apps.users.permissions import IsAdminOrHR
from .serializers import EmployeeOnboardingSerializer
from .models import Employee

User = get_user_model()

class EmployeeOnboardView(APIView):
    """
    API for Super Admin or HR to onboard a new employee.
    - Validates data
    - Creates an inactive User account
    - Generates a 24-hour invitation token
    - Creates an Employee profile linked to the User
    - Sends an invitation email to the console
    """
    permission_classes = [IsAdminOrHR]

    def post(self, request):
        serializer = EmployeeOnboardingSerializer(data=request.data)
        if serializer.is_valid():
            data = serializer.validated_data
            
            try:
                with transaction.atomic():
                    # 1. Create User (inactive)
                    user = User.objects.create_user(
                        email=data['email'],
                        role=data['role'],
                        is_active=False
                    )
                    
                    # 2. Generate Invite Token with 24h expiry
                    user.generate_invite_token(hours=24)
                    
                    # 3. Create Employee Profile
                    # Automatically generate an internal employee_id if not provided
                    emp_id = f"EMP-{user.id:04d}"
                    
                    employee = Employee.objects.create(
                        user=user,
                        employee_id=emp_id,
                        first_name=data['first_name'],
                        last_name=data['last_name'],
                        phone=data['phone'],
                        department=data['department'],
                        designation=data['designation'],
                        joining_date=data['joining_date'],
                        salary=data['salary'],
                        status='onboarding'
                    )
                    
                    # 4. Send Email (Simulated to Console)
                    activation_link = f"http://localhost:5173/activate?token={user.invite_token}"
                    subject = "Welcome to CODO HRM - Account Activation"
                    message = (
                        f"Hello {employee.first_name},\n\n"
                        f"Your account for CODO HRM has been created. "
                        f"Please activate your account by clicking the link below:\n\n"
                        f"{activation_link}\n\n"
                        f"This link will expire in 24 hours.\n\n"
                        f"Best regards,\nHR Department"
                    )
                    
                    send_mail(
                        subject,
                        message,
                        settings.DEFAULT_FROM_EMAIL,
                        [user.email],
                        fail_silently=False,
                    )
                    
                return Response({
                    "message": "Employee onboarded successfully. Invitation email sent.",
                    "data": {
                        "employee_id": emp_id,
                        "email": user.email,
                        "token": user.invite_token # For easier manual testing in dev
                    }
                }, status=status.HTTP_201_CREATED)
                
            except Exception as e:
                return Response({
                    "error": "Internal server error occurred during onboarding.",
                    "details": str(e)
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
