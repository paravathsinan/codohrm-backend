from rest_framework import viewsets, permissions
from .models import Project
from .serializers import ProjectSerializer

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        # Add basic filtering if needed (e.g. by enterprise)
        enterprise_id = self.request.query_params.get('enterprise')
        if enterprise_id:
            queryset = queryset.filter(enterprise_id=enterprise_id)
        return queryset
