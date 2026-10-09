from rest_framework import serializers
from .models import GeneratedReport

class GeneratedReportSerializer(serializers.ModelSerializer):
    author = serializers.CharField(source='generated_by.username', read_only=True)

    class Meta:
        model = GeneratedReport
        fields = '__all__'
