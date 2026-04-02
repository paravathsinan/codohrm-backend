from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    """
    Custom Admin for User model to handle email-only authentication and roles.
    """
    # Use email instead of username for the display
    list_display = ('email', 'role', 'is_active', 'is_staff')
    list_filter = ('is_active', 'is_staff', 'role')
    
    # Define fieldsets for editing existing users
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
        ('Custom data', {'fields': ('is_email_verified', 'invite_token', 'token_expiry')}),
    )
    
    # Define add_fieldsets for creating new users
    # This removes the username requirement from the admin creation form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'role', 'is_staff', 'is_active')
        }),
    )
    
    search_fields = ('email',)
    ordering = ('email',)
