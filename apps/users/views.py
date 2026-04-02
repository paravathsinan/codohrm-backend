from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import ActivateAccountSerializer, CustomTokenObtainPairSerializer
from .models import User

class LoginView(TokenObtainPairView):
    """
    Custom Login View that uses email instead of username.
    Returns access and refresh JSON web tokens.
    """
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [AllowAny]

class ActivateAccountView(APIView):
    """
    API for account activation using an invitation token.
    - Validates the token and its expiration
    - Sets the user's password
    - Activates the account
    - Clears security tokens to prevent reuse
    """
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = ActivateAccountSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            password = serializer.validated_data['password']
            
            try:
                # Find the user by the invitation token
                user = User.objects.get(invite_token=token)
                
                # Verify the token hasn't expired
                if user.token_expiry and user.token_expiry < timezone.now():
                    return Response({
                        "error": "This invitation link has expired."
                    }, status=status.HTTP_400_BAD_REQUEST)
                
                # Critical Update: Activate user and clear tracking tokens
                user.set_password(password)
                user.is_active = True
                user.is_email_verified = True
                user.invite_token = None
                user.token_expiry = None
                user.save()
                
                return Response({
                    "message": "Account activated successfully. You can now log in with your email and password."
                }, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:
                return Response({
                    "error": "Invalid or expired invitation token."
                }, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
