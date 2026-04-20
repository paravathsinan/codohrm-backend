from django.contrib import admin
from .models import Employee, EmployeeAddress, EmployeeBankDetail, EmployeeRole

admin.site.register(Employee)
admin.site.register(EmployeeAddress)
admin.site.register(EmployeeBankDetail)
admin.site.register(EmployeeRole)
