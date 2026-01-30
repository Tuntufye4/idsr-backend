# models.py (Django backend updated for full patient data model)
from django.db import models
from patients.models import PatientCase          

class Epidemiological_details(models.Model):
    patient_id = models.ForeignKey(    
        PatientCase,
        on_delete=models.SET_NULL,    
        null=True,            
        related_name='epidemiological_details'  # <-- unique reverse name    
    )  
    environmental_risk_factors = models.CharField(max_length=100, blank=True, null=True)
    exposure_source = models.CharField(max_length=200, blank=True, null=True)
    cluster_related = models.CharField(max_length=200, blank=True, null=True)        

    def __str__(self):      
        patient_name = self.patient_id.full_name if self.patient_id else "Unknown Patient"
        return f"{patient_name} ({self.id})"            
                                           