from rest_framework import viewsets
from .models import PatientCase
from .serializers import PatientCaseSerializer
from rest_framework.decorators import action  

class PatientCaseViewSet(viewsets.ModelViewSet):
    queryset = PatientCase.objects.all()
    serializer_class = PatientCaseSerializer
   
    def get_queryset(self):
        queryset = PatientCase.objects.all()
        sex = self.request.query_params.get('sex')
        region = self.request.query_params.get('region')   
        district = self.request.query_params.get('district')  
        village = self.request.query_params.get('village') 

        if sex:
            queryset = queryset.filter(sex__iexact=sex)

        if region:
            queryset = queryset.filter(region__icontains=region)

        if district:
            queryset = queryset.filter(district__icontains=district)

        if village:
            queryset = queryset.filter(village__icontains=village)


        return queryset
    