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
        vaccination_status = self.request.query_params.get('vaccination_status')
        health_facility = self.request.query_params.get('health_facility')   

        if sex:
            queryset = queryset.filter(sex__iexact=sex)

        if region:
            queryset = queryset.filter(region__icontains=region)

        if district:
            queryset = queryset.filter(district__icontains=district)

        if village:
            queryset = queryset.filter(village__icontains=village)

        if vaccination_status:
            queryset = queryset.filter(vaccination_status__icontains=vaccination_status)

        if health_facility:
            queryset = queryset.filter(health_facility__icontains=health_facility)


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


        # Case counts per vaccination status     

        data['vaccinationstatus'] = (
            PatientCase.objects.values('vaccination_status')
            .annotate(count=Count('id'))
            .order_by('-count')   
        )
        
        # Case counts per health facility   

        data['health_facility'] = (
            PatientCase.objects.values('health_facility')
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

        return Response(data)