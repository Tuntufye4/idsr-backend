from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from .models import Facility
from .serializers import FacilitySerializer
from patients.models import PatientCase

class FacilityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Facility cases:
    - Dynamic filtering
    - PATCH auto-creates a record if missing
    - Stats endpoint
    """
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer

    def get_queryset(self):
        queryset = Facility.objects.all()
        params = self.request.query_params

        # String filters
        string_fields = ['case_source', 'reporting_method', 'health_facility_code', 'designation']
        for field in string_fields:
            value = params.get(field)
            if value:
                queryset = queryset.filter(**{f"{field}__icontains": value})

        return queryset

    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        PATCH endpoint: create Facility record if it doesn't exist for patient_id
        """
        patient_id = request.data.get("patient_id")
        if not patient_id:
            return Response({"error": "patient_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient = PatientCase.objects.get(id=patient_id)
        except PatientCase.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get or create facility record for this patient
        facility_record, created = Facility.objects.get_or_create(patient_id=patient)

        serializer = FacilitySerializer(facility_record, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for Facility cases"""
        data = {}

        def count_dict(field):
            return {
                item[field]: item['count'] 
                for item in Facility.objects.values(field)
                        .annotate(count=Count('id'))
                        .order_by('-count')
            }

        for field in ['case_source', 'reporting_method', 'designation', 'health_facility_code']:
            data[field] = count_dict(field)

        return Response(data)
