from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Lab
from .serializers import LabSerializer

class LabViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Lab cases with:
    - Dynamic filtering
    - Stats endpoint for analytics/charts
    """
    queryset = Lab.objects.all()
    serializer_class = LabSerializer

    def get_queryset(self):
        queryset = Lab.objects.all()
        params = self.request.query_params

        # Filterable fields
        string_fields = [
            'specimen_type', 'lab_result', 'lab_tests_ordered', 
            'lab_name', 'specimen_collected', 'specimen_sent_to_lab'
        ]
        for field in string_fields:
            value = params.get(field)
            if value:
                queryset = queryset.filter(**{f"{field}__icontains": value})

        return queryset

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for Lab cases"""
        data = {}
  
        # Helper to return {key: count} dictionary
        def count_dict(field):
            return {item[field]: item['count'] for item in
                    Lab.objects.values(field)
                    .annotate(count=Count('id'))
                    .order_by('-count')}

        for field in ['specimen_type', 'lab_result', 'lab_tests_ordered',
                      'lab_name', 'specimen_collected', 'specimen_sent_to_lab']:
            data[field] = count_dict(field)

        return Response(data)
