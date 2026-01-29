from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from .models import SurveillanceInfo
from .serializers import SurveillanceSerializer
from patients.models import PatientCase  # assuming Surveillance links to a patient

class SurveillanceViewSet(viewsets.ModelViewSet):
    queryset = SurveillanceInfo.objects.all()
    serializer_class = SurveillanceSerializer

    def get_queryset(self):
        queryset = SurveillanceInfo.objects.all()
        params = self.request.query_params

        # Filters
        if year := params.get('year'):
            queryset = queryset.filter(year__iexact=year)
        if reviewed_by := params.get('reviewed_by'):
            queryset = queryset.filter(reviewed_by__iexact=reviewed_by)

        return queryset

    def partial_update(self, request, pk=None, *args, **kwargs):
        """
        PATCH endpoint: auto-create record if missing for patient
        """
        patient_id = request.data.get("patient_id")
        if not patient_id:
            return Response({"error": "patient_id is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            patient = PatientCase.objects.get(id=patient_id)
        except PatientCase.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        # Get or create Surveillance record for this patient
        surveillance_record, created = SurveillanceInfo.objects.get_or_create(patient_id=patient)

        serializer = SurveillanceSerializer(surveillance_record, data=request.data, partial=True)
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
