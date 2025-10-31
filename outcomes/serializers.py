from rest_framework import serializers
from .models import Outcome_details

class OutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Outcome_details  
        fields = "__all__"
    