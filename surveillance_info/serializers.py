from rest_framework import serializers
from .models import SurveillanceInfo

class SurveillanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = SurveillanceInfo  
        fields = "__all__"
         