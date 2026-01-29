from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count

from .models import PatientCase
from .serializers import PatientCaseSerializer
from clinical.models import ClinicalCase
from treatment.models import Treatment
from lab.models import Lab
from epidemiological.models import Epidemiological_details        
from facility.models import Facility
from surveillance_info.models import SurveillanceInfo

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

    def create(self, request, *args, **kwargs):
        # Create PatientCase
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()

        # Automatically create empty related sections
        ClinicalCase.objects.create(
            patient_id=patient,
            disease='',
            case_classification='',
            symptoms='',
            triage_level='',
            diagnosis_type='',
            final_case_classification='',
            admission_status='',
            contact_with_confirmed_case=False,
            recent_travel_history=False,
            travel_destination=''
        )

        Treatment.objects.create(
            patient_id=patient,
            treatment_given='',
            procedures_done='',
            follow_up_plan='',
            referral_facility=''
        )

        Lab.objects.create(
            patient_id=patient,
            specimen_collected=False,
            specimen_sent_to_lab=False,
            specimen_type='',
            lab_name='',
            lab_result='',
            lab_tests_ordered='',
        )

        Epidemiological_details.objects.create(
            patient_id=patient,
            environmental_risk_factors='',
            exposure_source='',
            cluster_related=''
        )

        Facility.objects.create(
            patient_id=patient,
            case_source='',
            reporting_method='',
            designation='',
            health_facility_code=''
        )

        SurveillanceInfo.objects.create(
            patient_id=patient,
            year=None,
            reporting_week_number=None,
            date_reported=None,
            notifier_signature='',
            reviewed_by='',
            supervisor_comments=''
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for Patient Case"""
        data = {}

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

        data['village'] = (
            PatientCase.objects.values('village')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        data['districts'] = (
            PatientCase.objects.values('district')
            .annotate(count=Count('id'))
            .order_by('-count')   
        )
        
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
    