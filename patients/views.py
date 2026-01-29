from rest_framework import viewsets
from .models import PatientCase
from .serializers import PatientCaseSerializer
from rest_framework.decorators import action  
from django.db.models import Count
from rest_framework.response import Response

class PatientCaseViewSet(viewsets.ModelViewSet):
    queryset = PatientCase.objects.all()
    serializer_class = PatientCaseSerializer      
       
    def get_queryset(self):
        queryset = PatientCase.objects.all()
        sex = self.request.query_params.get('sex')
        region = self.request.query_params.get('region')   
        district = self.request.query_params.get('district')  
        village = self.request.query_params.get('village')      
        traditional_authority = self.request.query_params.get('traditional_authority') 

        if sex:
            queryset = queryset.filter(sex__iexact=sex)

        if region:
            queryset = queryset.filter(region__icontains=region)

        if district:
            queryset = queryset.filter(district__icontains=district)

        if village:
            queryset = queryset.filter(village__icontains=village)

        if traditional_authority:
            queryset = queryset.filter(traditional_authority__icontains=traditional_authority)


        return queryset   

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for Patient Case"""
        data = {}

        # case counts  per gender

        data['sex'] = (
            PatientCase.objects.values('sex')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        data['age'] = (
            PatientCase.objects.values('age')
            .annotate(count=Count('id'))
            .order_by('-count')
        )   

        # Case counts per village

        data['village'] = (
            PatientCase.objects.values('village')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        # Case counts per district

        data['districts'] = (
            PatientCase.objects.values('district')
            .annotate(count=Count('id'))
            .order_by('-count')   
        )
        
        # Case counts per region

        data['region'] = (
            PatientCase.objects.values('region')
            .annotate(count=Count('id'))
            .order_by('-count')
        ) 
        
        data['traditional_authority'] = (
            PatientCase.objects.values('traditional_authority')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
            
        return Response(data)   