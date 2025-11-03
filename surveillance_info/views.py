from rest_framework import viewsets
from .models import SurveillanceInfo
from .serializers import SurveillanceSerializer
from rest_framework.decorators import action   

class SurveillanceViewSet(viewsets.ModelViewSet):
    queryset = SurveillanceInfo.objects.all()
    serializer_class = SurveillanceSerializer     

    def get_queryset(self):
        queryset = SurveillanceInfo.objects.all()
        year = self.request.query_params.get('year')
 

        if year:
            queryset = queryset.filter(year__iexact=year)


        return queryset
                              
