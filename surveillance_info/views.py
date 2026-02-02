from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from .models import SurveillanceInfo
from .serializers import SurveillanceSerializer
from patients.models import PatientCase  # assuming Surveillance links to a patient

class SurveillanceViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Surveillance info:
    - Dynamic filtering
    - PATCH by patient_id (auto-create if missing)
    - Stats endpoint
    """
    queryset = SurveillanceInfo.objects.all()
    serializer_class = SurveillanceSerializer

    def get_queryset(self):
        queryset = SurveillanceInfo.objects.all()
        params = self.request.query_params

        if year := params.get('year'):
            queryset = queryset.filter(year__iexact=year)
        if reviewed_by := params.get('reviewed_by'):
            queryset = queryset.filter(reviewed_by__iexact=reviewed_by)

        return queryset

    @action(
        detail=False,
        methods=['patch'],
        url_path=r'by-patient/(?P<patient_id>\d+)'
    )
    def patch_by_patient(self, request, patient_id=None):
        """
        PATCH by patient_id: create Surveillance record if missing, update fields.
        """    
        try:
            patient = PatientCase.objects.get(patient_id=patient_id)   
        except PatientCase.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get or create surveillance record for this patient         
        surveillance_record, _ = SurveillanceInfo.objects.get_or_create(patient_id=patient)

        # Only update provided fields
        data = {k: v for k, v in request.data.items() if v is not None}
        serializer = SurveillanceSerializer(surveillance_record, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Return summary counts for charts
        """
        data = {}
        for field in ['year', 'reviewed_by']:
            counts = SurveillanceInfo.objects.values(field).annotate(count=Count('id'))
            data[field] = {item[field]: item['count'] for item in counts}
        return Response(data)
