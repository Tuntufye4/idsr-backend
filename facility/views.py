from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from .models import Facility
from .serializers import FacilitySerializer

class FacilityViewSet(viewsets.ModelViewSet):
    """
    API endpoint for Facility cases with:
    - Dynamic filtering
    - Stats endpoint for analytics/charts
    """
    queryset = Facility.objects.all()
    serializer_class = FacilitySerializer

    def get_queryset(self):
        queryset = Facility.objects.all()
        params = self.request.query_params

        # Define fields that can be filtered
        string_fields = ['case_source', 'reporting_method', 'health_facility_code', 'designation']
        for field in string_fields:
            value = params.get(field)
            if value:
                queryset = queryset.filter(**{f"{field}__icontains": value})

        return queryset

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Return summary statistics for Facility cases"""
        data = {}

        # Helper to return {key: count} dictionary
        def count_dict(field):
            return {item[field]: item['count'] for item in
                    Facility.objects.values(field)
                    .annotate(count=Count('id'))
                    .order_by('-count')}

        for field in ['case_source', 'reporting_method', 'designation', 'health_facility_code']:
            data[field] = count_dict(field)

        return Response(data)
