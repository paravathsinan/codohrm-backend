from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Project, Client, Server, ProjectClassification
from .serializers import ProjectSerializer, ClientSerializer, ServerSerializer, ProjectClassificationSerializer

class ServerViewSet(viewsets.ModelViewSet):
    queryset = Server.objects.all().order_by('-created_at')
    serializer_class = ServerSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        enterprise_id = self.request.headers.get('X-Enterprise-ID')
        
        if enterprise_id and enterprise_id.isdigit():
            queryset = queryset.filter(Q(enterprise_id=enterprise_id) | Q(enterprise_id__isnull=True))
            
        return queryset

    def perform_create(self, serializer):
        enterprise_id = self.request.headers.get('X-Enterprise-ID')
        serializer.save(enterprise_id=enterprise_id)

class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all().order_by('-created_at')
    serializer_class = ClientSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        enterprise_id = self.request.headers.get('X-Enterprise-ID')
        
        if enterprise_id and enterprise_id.isdigit():
            queryset = queryset.filter(Q(enterprise_id=enterprise_id) | Q(enterprise_id__isnull=True))
            
        return queryset

    def perform_create(self, serializer):
        enterprise_id = self.request.headers.get('X-Enterprise-ID')
        serializer.save(enterprise_id=enterprise_id)

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        
        user = self.request.user
        enterprise_id = self.request.headers.get('X-Enterprise-ID')
        
        if hasattr(user, 'role') and user.role == 'staff':
            queryset = queryset.filter(
                Q(team_members__user=user) | 
                Q(project_lead__user=user) |
                Q(qa_testers__user=user)
            )
            
            if enterprise_id and enterprise_id.isdigit():
                queryset = queryset.filter(enterprise_id=enterprise_id)
                
            queryset = queryset.distinct()
            
        elif enterprise_id and enterprise_id.isdigit():
            # For admins, show enterprise projects + legacy (NULL) projects
            queryset = queryset.filter(Q(enterprise_id=enterprise_id) | Q(enterprise_id__isnull=True))
        else:
            # No enterprise ID provided, show everything (global admin view)
            pass
            
        return queryset

    def perform_create(self, serializer):
        enterprise_id = self.request.headers.get('X-Enterprise-ID')
        serializer.save(enterprise_id=enterprise_id)
class ProjectClassificationViewSet(viewsets.ModelViewSet):
    queryset = ProjectClassification.objects.all().order_by('name')
    serializer_class = ProjectClassificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        enterprise_id = self.request.headers.get('X-Enterprise-ID')
        
        if enterprise_id and enterprise_id.isdigit():
            queryset = queryset.filter(Q(enterprise_id=enterprise_id) | Q(enterprise_id__isnull=True))
            
        return queryset

    def perform_create(self, serializer):
        enterprise_id = self.request.headers.get('X-Enterprise-ID')
        serializer.save(enterprise_id=enterprise_id)
