from rest_framework import serializers
from .models import EmployeeTask, PerformanceSnapshot, KeyPerformanceScore, KeyResultIndicator

class EmployeeTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmployeeTask
        fields = ('id', 'title', 'status', 'notes', 'date')

class PerformanceSnapshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceSnapshot
        fields = ('id', 'period', 'date', 'rating', 'feedback')

class KeyPerformanceScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyPerformanceScore
        fields = ('id', 'metric', 'score', 'target', 'last_updated')

class KeyResultIndicatorSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyResultIndicator
        fields = ('id', 'indicator', 'value', 'status')
