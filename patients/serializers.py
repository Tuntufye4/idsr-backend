from rest_framework import serializers
from .models import PatientCase  

class PatientCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientCase
        fields = "__all__"
   