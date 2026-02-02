from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django.db.models import Count
from .models import Treatment
from .serializers import TreatmentSerializer
from patients.models import PatientCase

class TreatmentViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Treatment cases:
    - Dynamic filtering
    - PATCH by patient_id (auto-create if missing)
    - Stats endpoint
    """
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer

    def get_queryset(self):
        queryset = Treatment.objects.all()
        params = self.request.query_params

        string_fields = ['treatment_given', 'procedures_done', 'follow_up_plan', 'referral_facility']
        for field in string_fields:
            value = params.get(field)
            if value:
                queryset = queryset.filter(**{f"{field}__icontains": value})

        return queryset

    @action(
        detail=False,
        methods=['patch'],
        url_path=r'by-patient/(?P<patient_id>\d+)'
    )
    def patch_by_patient(self, request, patient_id=None):
        """
        PATCH by patient_id: create Treatment record if missing, update fields.
        """    
        try:
            patient = PatientCase.objects.get(patient_id=patient_id)
        except PatientCase.DoesNotExist:
            return Response({"error": "Patient not found"}, status=status.HTTP_404_NOT_FOUND)

        treatment_record, _ = Treatment.objects.get_or_create(patient_id=patient)   

        data = {k: v for k, v in request.data.items() if v is not None}
        serializer = TreatmentSerializer(treatment_record, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()   
        return Response(serializer.data)   
           
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Return summary counts for charts
        """
        data = {}
        for field in ['treatment_given', 'procedures_done', 'follow_up_plan', 'referral_facility']:
            counts = Treatment.objects.values(field).annotate(count=Count('id'))
            data[field] = {item[field]: item['count'] for item in counts}
        return Response(data)
          