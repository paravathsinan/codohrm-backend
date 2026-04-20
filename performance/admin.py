from django.contrib import admin
from .models import EmployeeTask, PerformanceSnapshot, KeyPerformanceScore, KeyResultIndicator

admin.site.register(EmployeeTask)
admin.site.register(PerformanceSnapshot)
admin.site.register(KeyPerformanceScore)
admin.site.register(KeyResultIndicator)
