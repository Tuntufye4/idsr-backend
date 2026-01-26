from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count, Avg, Min, Max
from .models import ClinicalCase
from .serializers import ClinicalCaseSerializer      

class ClinicalCaseViewSet(viewsets.ModelViewSet): 
    queryset = ClinicalCase.objects.all()   
    serializer_class = ClinicalCaseSerializer   

    def get_queryset(self):
        queryset = ClinicalCase.objects.all()   
        symptoms = self.request.query_params.get('symptoms')
        triage_level = self.request.query_params.get('triage_level')   
        diagnosis_type = self.request.query_params.get('diagnosis_type')
        admission_status = self.request.query_params.get('admission_status')
        final_case_classification = self.request.query_params.get('final_case_classification')
        contact_with_confirmed_case = self.request.query_params.get('contact_with_confirmed_case')
        case_classification = self.request.query_params.get('case_classification')
        disease = self.request.query_params.get('disease')
        recent_travel_history = self.request.query_params.get('recent_travel_history')
        travel_destination = self.request.query_params.get('travel_destination')


        if symptoms:
            queryset = queryset.filter(symptoms__icontains=symptoms)

        if triage_level:
            queryset = queryset.filter(triage_level__icontains=triage_level)

        if diagnosis_type:
            queryset = queryset.filter(diagnosis_type__icontains=diagnosis_type)

        if admission_status:
            queryset = queryset.filter(admission_status__icontains=admission_status)

        if final_case_classification:
            queryset = queryset.filter(final_case_classification__icontains=final_case_classification)

        if contact_with_confirmed_case:
            queryset = queryset.filter(contact_with_confirmed_case__icontains=contact_with_confirmed_case)

        if case_classification:
            queryset = queryset.filter(case_classification__icontains=case_classification)
   
        if disease:
            queryset = queryset.filter(disease__icontains=disease)

        if recent_travel_history:
            queryset = queryset.filter(recent_travel_history__icontains=recent_travel_history)
        
        if travel_destination:
            queryset = queryset.filter(travel_destination__icontains=travel_destination)

        return queryset
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for Clinical case"""
        data = {}

        # Case counts per symptoms  
        
        data['symptoms'] = (
            ClinicalCase.objects.values('symptoms')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        # Case counts per triage level

        data['triagelevel'] = (
            ClinicalCase.objects.values('triage_level')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        # Case counts per diagnosis_type

        data['diagnosistype'] = (
            ClinicalCase.objects.values('diagnosis_type')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        # Case counts per case classification
        
        data['caseclassification'] = (
            ClinicalCase.objects.values('case_classification')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        data['final_caseclassification'] = (
            ClinicalCase.objects.values('final_case_classification')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        # Case counts per admission status
        
        data['admissionstatus'] = (
            ClinicalCase.objects.values('admission_status')
            .annotate(count=Count('id'))
            .order_by('-count')     
        )

        data['contactwithconfirmedcase'] = (
            ClinicalCase.objects.values('contact_with_confirmed_case')
            .annotate(count=Count('id'))
            .order_by('-count')    
        )
             

        data['traveldestination'] = (
            ClinicalCase.objects.values('travel_destination')
            .annotate(count=Count('id'))
            .order_by('-count')
        )    

        
        data['recenttravelhistory'] = (
            ClinicalCase.objects.values('recent_travel_history')
            .annotate(count=Count('id'))
            .order_by('-count')
        )   

        data['diseases'] = (
            ClinicalCase.objects.values('disease')
            .annotate(count=Count('id'))
            .order_by('-count')
        )

        return Response(data)    
   
    