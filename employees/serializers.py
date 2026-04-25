from rest_framework import serializers
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from users.serializers import UserSerializer
from .models import (
    Employee, EmployeeAddress, EmployeeBankDetail, EmployeeRole,
    Enterprise, Department, Position, WorkingMode, EmploymentType, SystemRole
)
from attendance.serializers import AttendanceRecordSerializer
from finance.serializers import ReimbursementSerializer
from leaves.serializers import LeaveBalanceSerializer
from performance.serializers import (
    EmployeeTaskSerializer, 
    PerformanceSnapshotSerializer, 
    KeyPerformanceScoreSerializer, 
    KeyResultIndicatorSerializer
)
from core.utils import send_whatsapp_message

User = get_user_model()

class EmployeeAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeAddress
        fields = ('id', 'house_name', 'city', 'post_office', 'pin_code', 'district', 'state')

class EmployeeBankDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeBankDetail
        fields = ('id', 'account_name', 'bank_name', 'account_number', 'ifsc', 'branch_name', 'account_type', 'upi_id', 'upi_phone_number')

class EnterpriseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enterprise
        fields = ('id', 'name', 'description')

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = ('id', 'enterprise', 'name')

class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = ('id', 'enterprise', 'name')

class WorkingModeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkingMode
        fields = ('id', 'name')

class EmploymentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmploymentType
        fields = ('id', 'name')

class SystemRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemRole
        fields = ('id', 'name')

class EmployeeRoleSerializer(serializers.ModelSerializer):
    # For data consistency, we'll return name strings in read ops but accept IDs for writes
    enterprise_name = serializers.ReadOnlyField(source='enterprise.name')
    department_name = serializers.ReadOnlyField(source='department.name')
    position_name = serializers.ReadOnlyField(source='position.name')
    reported_to_name = serializers.ReadOnlyField(source='reported_to.full_name')
    working_mode_name = serializers.ReadOnlyField(source='working_mode.name')
    employment_type_name = serializers.ReadOnlyField(source='employment_type.name')

    class Meta:
        model = EmployeeRole
        fields = (
            'id', 'enterprise', 'enterprise_name', 'department', 'department_name', 
            'position', 'position_name', 'reported_to', 'reported_to_name', 'working_mode', 
            'working_mode_name', 'employment_type', 'employment_type_name', 'working_hour', 
            'work_days', 'hourly_payment', 'joining_date', 'is_primary'
        )

class EmployeeSerializer(serializers.ModelSerializer):
    # Nested representation matching frontend interfaces
    email = serializers.EmailField(write_only=True, required=False)
    role = serializers.ChoiceField(choices=User.ROLE_CHOICES, write_only=True, required=False, default='staff')
    password = serializers.CharField(write_only=True, required=False)
    
    user = UserSerializer(read_only=True)
    address = EmployeeAddressSerializer(required=False)
    bank_details = EmployeeBankDetailSerializer(required=False)
    roles = EmployeeRoleSerializer(many=True, required=False)

    # Related data (Read Only)
    primary_department_name = serializers.SerializerMethodField()
    primary_position_name = serializers.SerializerMethodField()
    primary_enterprise_name = serializers.SerializerMethodField()
    primary_hourly_payment = serializers.SerializerMethodField()

    attendance_status = serializers.SerializerMethodField()

    attendance = AttendanceRecordSerializer(many=True, read_only=True)
    reimbursements = ReimbursementSerializer(many=True, read_only=True)
    tasks = EmployeeTaskSerializer(many=True, read_only=True)
    performance = PerformanceSnapshotSerializer(many=True, read_only=True, source='performance_snapshots')
    kps = KeyPerformanceScoreSerializer(many=True, read_only=True)
    kri = KeyResultIndicatorSerializer(many=True, read_only=True)
    leave_balances = LeaveBalanceSerializer(many=True, read_only=True)
    assigned_projects = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Employee
        fields = '__all__'
        read_only_fields = (
            'user', 'attendance', 'reimbursements', 'tasks', 'performance', 
            'kps', 'kri', 'leave_balances', 'assigned_projects',
            'primary_department_name', 'primary_position_name', 'primary_enterprise_name', 'primary_hourly_payment',
            'attendance_status'
        )

    def get_primary_department_name(self, obj):
        first_role = obj.roles.first()
        if first_role and first_role.department:
            return first_role.department.name
        return None

    def get_primary_position_name(self, obj):
        first_role = obj.roles.first()
        if first_role and first_role.position:
            return first_role.position.name
        return None

    def get_primary_enterprise_name(self, obj):
        first_role = obj.roles.first()
        if first_role and first_role.enterprise:
            return first_role.enterprise.name
        return None

    def get_primary_hourly_payment(self, obj):
        first_role = obj.roles.first()
        if first_role:
            return first_role.hourly_payment
        return 0

    def get_attendance_status(self, obj):
        today = timezone.localtime(timezone.now()).date()
        # Fetch only the status of the record for today
        # We use .filter().first() to avoid loading all attendance records
        record = obj.attendance.filter(date=today).first()
        if record:
            return record.status
        return 'Absent'

    def validate_email(self, value):
        """Check if a User with this email already exists, excluding current user for updates."""
        queryset = User.objects.filter(email=value)
        if self.instance and self.instance.user:
            queryset = queryset.exclude(id=self.instance.user.id)
            
        if value and queryset.exists():
            raise serializers.ValidationError("A user with this email already exists.")
        
        # Also check if the derived username would be duplicate
        username = value.split('@')[0] if value else None
        user_queryset = User.objects.filter(username=username)
        if self.instance and self.instance.user:
            user_queryset = user_queryset.exclude(id=self.instance.user.id)
            
        if username and user_queryset.exists():
            raise serializers.ValidationError(f"The username '{username}' (derived from email) is already taken. Please use a different email or provide a custom username.")
        
        return value

    @transaction.atomic
    def create(self, validated_data):
        address_data = validated_data.pop('address', None)
        bank_details_data = validated_data.pop('bank_details', None)
        roles_data = validated_data.pop('roles', [])
        
        # User details matching
        email = validated_data.pop('email', f"user_{validated_data.get('phone_number')}@codohrm.local")
        role = validated_data.pop('role', 'staff')
        
        # Create User
        username = email.split('@')[0] if email else validated_data.get('phone_number')
        password = validated_data.pop('password', None)
        
        user = User.objects.create(username=username, email=email, role=role)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save()

        # Create Employee
        employee = Employee.objects.create(user=user, **validated_data)

        # Send Onboarding Notifications
        if password and employee.phone_number:
            self._send_onboarding_whatsapp(employee, password)
            
        if password and email:
            self._send_onboarding_email(employee, password)

        # Handle Nested Data
        if address_data:
            EmployeeAddress.objects.create(employee=employee, **address_data)
        if bank_details_data:
            EmployeeBankDetail.objects.create(employee=employee, **bank_details_data)
        
        for role_data in roles_data:
            EmployeeRole.objects.create(employee=employee, **role_data)
        
        return employee

    @transaction.atomic
    def update(self, instance, validated_data):
        # Handle nested User updates (Email/Role)
        user_data = {}
        if 'email' in validated_data:
            user_data['email'] = validated_data.pop('email')
            user_data['username'] = user_data['email'].split('@')[0]
        if 'role' in validated_data:
            user_data['role'] = validated_data.pop('role')

        if user_data and instance.user:
            for attr, value in user_data.items():
                setattr(instance.user, attr, value)
            instance.user.save()

        address_data = validated_data.pop('address', None)
        bank_details_data = validated_data.pop('bank_details', None)
        roles_data = validated_data.pop('roles', None)

        # Update base fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update nested address
        if address_data is not None:
            if hasattr(instance, 'address'):
                for attr, value in address_data.items():
                    setattr(instance.address, attr, value)
                instance.address.save()
            else:
                EmployeeAddress.objects.create(employee=instance, **address_data)

        # Update nested bank details
        if bank_details_data is not None:
            if hasattr(instance, 'bank_details'):
                for attr, value in bank_details_data.items():
                    setattr(instance.bank_details, attr, value)
                instance.bank_details.save()
            else:
                EmployeeBankDetail.objects.create(employee=instance, **bank_details_data)

        # Update roles (usually replace all)
        if roles_data is not None:
            instance.roles.all().delete()
            for role_data in roles_data:
                EmployeeRole.objects.create(employee=instance, **role_data)

        return instance

    def _send_onboarding_email(self, employee, password):
        subject = f"Welcome to CODO HRM - Your Account is Ready"
        from_email = settings.DEFAULT_FROM_EMAIL
        to = employee.user.email
        
        context = {
            'full_name': employee.full_name,
            'email': employee.user.email,
            'password': password,
            'login_url': 'http://localhost:5173/login'
        }
        
        html_content = render_to_string('emails/onboarding_email.html', context)
        text_content = strip_tags(html_content)
        
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    def _send_onboarding_whatsapp(self, employee, password):
        """
        Send a welcome WhatsApp message to the new employee.
        """
        message = (
            f"Welcome to CODO HRM, *{employee.full_name}*! \n\n"
            f"Your employee account has been successfully deployed. \n\n"
            f"🔑 *Credentials:* \n"
            f"Work Email: {employee.user.email} \n"
            f"Password: {password} \n\n"
            f"Please login at: http://localhost:5173/login to complete your onboarding records. \n\n"
            f"Regards, \n"
            f"HR Team, CODO AI Innovations"
        )
        
        # Use the phone number from the employee record
        if employee.phone_number:
            send_whatsapp_message(employee.phone_number, message)
