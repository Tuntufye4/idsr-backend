from rest_framework import serializers
from .models import Epidemiological_details

class EpidemiologicalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Epidemiological_details  
        fields = "__all__"
       