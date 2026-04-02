from django.contrib import admin
from .models import Employee

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    """
    Admin configuration for Employee model.
    """
    list_display = (
        'employee_id', 
        'first_name', 
        'last_name', 
        'department', 
        'designation', 
        'status'
    )
    list_filter = ('status', 'department', 'designation')
    search_fields = ('employee_id', 'first_name', 'last_name', 'phone')
    ordering = ('employee_id',)
    
    # Optional: fieldsets for better organization in the edit view
    fieldsets = (
        ('Personal Info', {
            'fields': ('user', 'employee_id', 'first_name', 'last_name', 'phone')
        }),
        ('Professional Info', {
            'fields': ('department', 'designation', 'joining_date', 'salary', 'status')
        }),
        ('Dates', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    readonly_fields = ('created_at', 'updated_at')
