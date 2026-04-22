from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils import timezone
from .models import AttendanceRecord, AttendanceBreak
from .serializers import AttendanceRecordSerializer, AttendanceBreakSerializer
from employees.models import Employee
from performance.models import EmployeeTask

class AttendanceViewSet(viewsets.ModelViewSet):
    serializer_class = AttendanceRecordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        date_param = self.request.query_params.get('date')
        queryset = AttendanceRecord.objects.all()
        
        if date_param:
            queryset = queryset.filter(date=date_param)
            
        if self.request.user.role in ['superadmin', 'hr']:
            return queryset
        
        return queryset.filter(employee__user=self.request.user)

    def perform_create(self, serializer):
        employee = Employee.objects.get(user=self.request.user)
        # Use server-side local date for consistency
        today = timezone.localtime(timezone.now()).date()
        
        existing = AttendanceRecord.objects.filter(employee=employee, date=today).first()
        planned_work = serializer.validated_data.get('planned_work', 'Daily Update')
        
        if existing:
            serializer.instance = existing
            serializer.save(status='Present', date=today)
        else:
            serializer.save(employee=employee, status='Present', date=today)

        # Auto-create EmployeeTask (Daily Update) for "Saved Submissions"
        EmployeeTask.objects.get_or_create(
            employee=employee,
            date=today,
            title=planned_work,
            defaults={'status': 'Ongoing'}
        )

    def perform_update(self, serializer):
        serializer.save()

    @action(detail=False, methods=['get'])
    def today(self, request):
        try:
            employee = Employee.objects.get(user=request.user)
            # Use local date instead of UTC to match frontend expectations
            today = timezone.localtime(timezone.now()).date()
            record = AttendanceRecord.objects.filter(employee=employee, date=today).first()
            
            if record:
                serializer = self.get_serializer(record)
                return Response(serializer.data)
            return Response(None, status=status.HTTP_200_OK)
        except Employee.DoesNotExist:
            return Response({"detail": "Employee profile not found"}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post'])
    def start_break(self, request, pk=None):
        record = self.get_object()
        break_rec = AttendanceBreak.objects.create(
            attendance_record=record,
            start_time=timezone.now()
        )
        record.status = 'Break'
        record.save()
        return Response(AttendanceBreakSerializer(break_rec).data)

    @action(detail=True, methods=['post'])
    def end_break(self, request, pk=None):
        record = self.get_object()
        break_rec = record.breaks.filter(end_time__isnull=True).last()
        
        if break_rec:
            break_rec.end_time = timezone.now()
            duration = (break_rec.end_time - break_rec.start_time).total_seconds()
            break_rec.duration_seconds = int(duration)
            break_rec.save()
            
            record.status = 'Present'
            record.total_break_seconds += int(duration)
            record.save()
            
            return Response(AttendanceBreakSerializer(break_rec).data)
        return Response({"detail": "No active break found"}, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Also clean up the auto-generated task for this day
        EmployeeTask.objects.filter(
            employee=instance.employee, 
            date=instance.date
        ).delete()
        return super().destroy(request, *args, **kwargs)
