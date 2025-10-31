from rest_framework import viewsets
from .models import Treatment
from .serializers import TreatmentSerializer   
from rest_framework.decorators import action  

class TreatmentViewSet(viewsets.ModelViewSet):
    queryset = Treatment.objects.all()
    serializer_class = TreatmentSerializer  

    def get_queryset(self):
        queryset = Treatment.objects.all()   
        procedures_done  = self.request.query_params.get('procedures_done')
        follow_up_plan = self.request.query_params.get('follow_up_plan')     

        if procedures_done:
            queryset = queryset.filter(procedures_done__iexact=procedures_done)

        if follow_up_plan:
            queryset = queryset.filter(follow_up_plan__icontains=follow_up_plan)

        return queryset                                    