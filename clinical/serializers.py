from rest_framework import serializers
from .models import ClinicalCase

class ClinicalCaseSerializer(serializers.ModelSerializer):
    # Booleans: allow null so PATCH can skip them
    contact_with_confirmed_case = serializers.BooleanField(required=False, allow_null=True)
    recent_travel_history = serializers.BooleanField(required=False, allow_null=True)
    
    # Date: allow null
    date_of_onset = serializers.DateField(required=False, allow_null=True)
                
    class Meta:
        model = ClinicalCase
        fields = "__all__"
   