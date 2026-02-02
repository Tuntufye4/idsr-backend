from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from .models import ClinicalCase
from .serializers import ClinicalCaseSerializer
from patients.models import PatientCase

class ClinicalCaseViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Clinical Cases:
    - Dynamic filtering via query params
    - PATCH endpoint by patient_id (creates if missing)
    - Stats endpoint for charts   
    """
    queryset = ClinicalCase.objects.all()
    serializer_class = ClinicalCaseSerializer

    def get_queryset(self):
        queryset = ClinicalCase.objects.all()
        params = self.request.query_params

        # --- String filters ---
        string_fields = [
            'symptoms', 'triage_level', 'diagnosis_type', 'admission_status',
            'final_case_classification', 'case_classification', 'disease',
            'travel_destination'
        ]
        for field in string_fields:
            val = params.get(field)
            if val:
                queryset = queryset.filter(**{f"{field}__icontains": val})

        # --- Boolean filters ---
        bool_fields = ['contact_with_confirmed_case', 'recent_travel_history']
        for field in bool_fields:
            val = params.get(field)
            if val is not None:
                val_bool = val.lower() in ['true', '1', 'yes']
                queryset = queryset.filter(**{field: val_bool})
     
        return queryset

    @action(
        detail=False,
        methods=['patch'],
        url_path=r'by-patient/(?P<patient_id>\d+)'
    )
    def patch_by_patient(self, request, patient_id=None):
        """
        PATCH by patient_id: creates record if missing, updates fields.
        Handles booleans and nullable dates safely.
        """
        # --- Get patient ---
        try:
            patient = PatientCase.objects.get(patient_id=patient_id)
        except PatientCase.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        # --- Get or create clinical case ---
        clinical_case, _ = ClinicalCase.objects.get_or_create(patient_id=patient)

        # --- Clean and preprocess input data ---
        data = {k: v for k, v in request.data.items() if v is not None}

        # Preprocess booleans
        for bool_field in ['contact_with_confirmed_case', 'recent_travel_history']:
            if bool_field in data:
                val = data[bool_field]
                if isinstance(val, str):
                    data[bool_field] = val.lower() in ['true', '1', 'yes']
                else:
                    data[bool_field] = bool(val)

        # Preprocess nullable date fields
        date_fields = ['date_of_onset']
        for date_field in date_fields:
            if date_field in data and data[date_field] in [None, '', 'null']:
                data[date_field] = None

        # --- Serialize and save ---
        serializer = ClinicalCaseSerializer(clinical_case, data=data, partial=True)
        if not serializer.is_valid():
            # Debug: print validation errors
            print("ClinicalCase PATCH validation errors:", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for charts"""
        data = {}

        def count_dict(field):
            return {
                item[field]: item['count']
                for item in ClinicalCase.objects.values(field)
                        .annotate(count=Count('id'))
                        .order_by('-count')
            }

        # --- String fields ---
        string_fields = [
            'symptoms', 'triage_level', 'diagnosis_type',
            'case_classification', 'final_case_classification',
            'admission_status', 'disease', 'travel_destination'
        ]
        for field in string_fields:
            data[field] = count_dict(field)

        # --- Boolean fields ---
        bool_fields = ['contact_with_confirmed_case', 'recent_travel_history']
        for field in bool_fields:
            counts = ClinicalCase.objects.values(field).annotate(count=Count('id'))
            data[field] = {str(item[field]): item['count'] for item in counts}

        return Response(data)
