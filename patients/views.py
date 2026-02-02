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
        # Dynamic filtering: only apply filters that exist
        for field in ['sex', 'region', 'district', 'village', 'traditional_authority']:
            value = self.request.query_params.get(field)
            if value:
                queryset = queryset.filter(**{f"{field}__iexact": value})
        return queryset

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        patient = serializer.save()

        # Automatically create empty related sections if they don't exist
        related_models = [
            (ClinicalCase, {
                'disease': '', 'date_of_onset': None, 'case_classification': '', 
                'symptoms': '', 'triage_level': '', 'diagnosis_type': '', 
                'final_case_classification': '', 'admission_status': '', 
                'contact_with_confirmed_case': False, 'recent_travel_history': False, 
                'travel_destination': ''
            }),
            (Treatment, {'treatment_given': '', 'procedures_done': '', 'follow_up_plan': '', 'referral_facility': ''}),
            (Lab, {'specimen_collected': False, 'specimen_sent_to_lab': False, 'date_specimen_collected': None, 
                   'specimen_type': '', 'lab_name': '', 'lab_result': '', 'lab_tests_ordered': ''}),
            (Epidemiological_details, {'environmental_risk_factors': '', 'exposure_source': '', 'cluster_related': ''}),
            (Facility, {'date_reported': None, 'case_source': '', 'reporting_method': '', 'designation': '', 
                       'health_facility_code': '', 'form_completed_by': ''}),
            (SurveillanceInfo, {'year': None, 'reporting_week_number': None, 'date_reported': None, 
                                'notifier_signature': '', 'reviewed_by': '', 'supervisor_comments': ''})
        ]    

        for model, defaults in related_models:
            model.objects.get_or_create(patient_id=patient, defaults=defaults)

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for PatientCase"""
        data = {}
        for field in ['sex', 'age', 'village', 'district', 'region', 'traditional_authority']:
            counts = PatientCase.objects.values(field).annotate(count=Count('id')).order_by('-count')
            data[field] = {item[field]: item['count'] for item in counts}
        return Response(data)
