from rest_framework import serializers
from .models import Project
class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = '__all__'
        extra_kwargs = {
            'team_members': {'required': False},
            'qa_testers': {'required': False},
        }

    def get_fields(self):
        fields = super().get_fields()
        from employees.serializers import EmployeeSerializer
        fields['team_members_detail'] = EmployeeSerializer(source='team_members', many=True, read_only=True)
        fields['qa_testers_detail'] = EmployeeSerializer(source='qa_testers', many=True, read_only=True)
        fields['project_lead_detail'] = EmployeeSerializer(source='project_lead', read_only=True)
        return fields

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Flatten team member details for the frontend if needed
        # but keep standard IDs for write operations
        return representation
