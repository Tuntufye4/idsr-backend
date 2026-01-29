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
    - PATCH endpoint auto-creates row if it doesn't exist
    - Stats endpoint for charts
    """
    queryset = ClinicalCase.objects.all()
    serializer_class = ClinicalCaseSerializer

    def get_queryset(self):
        queryset = ClinicalCase.objects.all()
        params = self.request.query_params

        # String filters
        string_fields = [
            'symptoms', 'triage_level', 'diagnosis_type', 'admission_status',
            'final_case_classification', 'case_classification', 'disease',
            'travel_destination'
        ]
        for field in string_fields:
            value = params.get(field)
            if value:
                queryset = queryset.filter(**{f"{field}__icontains": value})

        # Boolean filters
        bool_fields = ['contact_with_confirmed_case', 'recent_travel_history']
        for field in bool_fields:
            val = params.get(field)
            if val is not None:
                val_bool = val.lower() in ['true', '1', 'yes']
                queryset = queryset.filter(**{field: val_bool})

        return queryset

    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        PATCH endpoint: create ClinicalCase if it doesn't exist for patient_id,
        then apply updates.
        """
        patient_id = request.data.get("patient_id")
        if not patient_id:
            return Response({"error": "patient_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient = PatientCase.objects.get(id=patient_id)
        except PatientCase.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get or create the ClinicalCase for this patient
        clinical_case, created = ClinicalCase.objects.get_or_create(patient_id=patient)

        serializer = ClinicalCaseSerializer(clinical_case, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for charts"""
        data = {}

        # Helper function for generating counts dict
        def count_dict(field):
            return {
                item[field]: item['count']
                for item in ClinicalCase.objects.values(field).annotate(count=Count('id')).order_by('-count')
            }

        # String fields
        for field in [
            'symptoms', 'triage_level', 'diagnosis_type',
            'case_classification', 'final_case_classification',
            'admission_status', 'disease', 'travel_destination'
        ]:
            data[field] = count_dict(field)

        # Boolean fields    
        for field in ['contact_with_confirmed_case', 'recent_travel_history']:
            counts = ClinicalCase.objects.values(field).annotate(count=Count('id'))
            # Convert True/False to Yes/No for frontend readability
            data[field] = {str(item[field]): item['count'] for item in counts}

        return Response(data)
