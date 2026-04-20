from django.contrib import admin
from .models import AttendanceRecord, AttendanceBreak

admin.site.register(AttendanceRecord)
admin.site.register(AttendanceBreak)
