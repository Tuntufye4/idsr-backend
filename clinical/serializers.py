from rest_framework import serializers
from .models import ClinicalCase  

class ClinicalCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicalCase
        fields = "__all__"
    