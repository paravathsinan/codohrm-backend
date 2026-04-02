from rest_framework import serializers
from django.contrib.auth import get_user_model
from apps.roles.models import Role

User = get_user_model()

class EmployeeOnboardingSerializer(serializers.Serializer):
    """
    Serializer to validate data for initial employee onboarding.
    Does not create any database records; only performs validation.
    """
    email = serializers.EmailField()
    role = serializers.PrimaryKeyRelatedField(queryset=Role.objects.all())
    
    first_name = serializers.CharField(max_length=100)
    last_name = serializers.CharField(max_length=100)
    phone = serializers.CharField(max_length=20)
    
    department = serializers.CharField(max_length=100)
    designation = serializers.CharField(max_length=100)
    
    joining_date = serializers.DateField()
    salary = serializers.DecimalField(max_digits=10, decimal_places=2)

    def validate_email(self, value):
        """
        Check that the email is unique in the User model.
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with this email already exists.")
        return value
