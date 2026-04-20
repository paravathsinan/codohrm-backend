from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role', 'is_active', 'date_joined')
        read_only_fields = ('id', 'date_joined')

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import authenticate

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = 'email'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Change username to email
        self.fields['email'] = serializers.EmailField()
        if 'username' in self.fields:
            del self.fields['username']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(request=self.context.get('request'), username=email, password=password)
        if not user:
            # Fallback to authenticating with email using a custom check if Django uses 'username' field
            try:
                user_obj = User.objects.get(email=email)
                user = authenticate(request=self.context.get('request'), username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if not user or not user.is_active:
            raise serializers.ValidationError('No active account found with the given credentials')

        self.user = user

        refresh = self.get_token(self.user)

        data = {}
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)
        data['role'] = self.user.role
        
        return data
