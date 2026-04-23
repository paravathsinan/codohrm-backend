from rest_framework import serializers
from .models import Project
from employees.serializers import EmployeeSerializer

class ProjectSerializer(serializers.ModelSerializer):
    # For GET requests, we want detailed employee info
    team_members_detail = EmployeeSerializer(source='team_members', many=True, read_only=True)
    qa_testers_detail = EmployeeSerializer(source='qa_testers', many=True, read_only=True)
    project_lead_detail = EmployeeSerializer(source='project_lead', read_only=True)

    class Meta:
        model = Project
        fields = '__all__'
        extra_kwargs = {
            'team_members': {'required': False},
            'qa_testers': {'required': False},
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Flatten team member details for the frontend if needed
        # but keep standard IDs for write operations
        return representation
