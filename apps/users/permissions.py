from rest_framework.permissions import BasePermission

class IsAdminOrHR(BasePermission):
    """
    Custom permission for access by Super Admin or HR roles.
    Logic:
    - Grant access if user is authenticated AND
    - user's role is 'Super Admin' or 'HR'
    """

    def has_permission(self, request, view):
        # 1. Check if user is authenticated
        if not (request.user and request.user.is_authenticated):
            return False
        
        # 2. Check if role exists and matches allowed roles
        if not request.user.role:
            return False
        
        # We use role.name case-insensitively just in case, but usually strict match is better
        allowed_roles = ['Super Admin', 'HR']
        return request.user.role.name in allowed_roles
