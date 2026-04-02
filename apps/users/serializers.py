from django.utils import timezone
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom JWT Serializer that takes 'email' instead of 'username'.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Rename the 'username' field to 'email' for the API interface
        self.fields['email'] = serializers.EmailField()
        if 'username' in self.fields:
            del self.fields['username']

    def validate(self, attrs):
        # Log attempt
        with open('login_debug.log', 'a') as f:
            f.write(f"Login attempt at {timezone.now()}: {attrs.get('email')}\n")
            
        # The base class uses self.username_field (which is 'email') to authenticate.
        # Since we renamed the field to 'email' in __init__, attrs already has 'email'.
        try:
            data = super().validate(attrs)
            with open('login_debug.log', 'a') as f:
                f.write(f"Success for {attrs.get('email')}\n")
            
            # Include the user's role in the response (normalized for frontend)
            role_map = {
                'Super Admin': 'superadmin',
                'HR': 'hr',
                'Finance': 'finance',
            }
            
            if self.user.role:
                db_role = self.user.role.name
                data['role'] = role_map.get(db_role, 'staff') # Default to 'staff' if not in map
            else:
                # Default to staff if no role is assigned
                data['role'] = 'staff'
            
            return data
        except Exception as e:
            with open('login_debug.log', 'a') as f:
                f.write(f"Failure for {attrs.get('email')}: {str(e)}\n")
            raise e

class ActivateAccountSerializer(serializers.Serializer):
    """
    Serializer for account activation.
    Validates the invitation token and the new password.
    """
    token = serializers.CharField(required=True)
    password = serializers.CharField(
        required=True, 
        min_length=8, 
        write_only=True,
        style={'input_type': 'password'}
    )
