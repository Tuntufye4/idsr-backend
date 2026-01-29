# models.py (Django backend updated for full patient data model)
import uuid   
from django.db import models
from patients.models import PatientCase

class Outcome_details(models.Model):
    patient_id = models.ForeignKey(    
        PatientCase,
        on_delete=models.SET_NULL,    
        null=True,            
        related_name='outcomes'  # <-- unique reverse name    
    )  
    outcome = models.CharField(max_length=100, blank=True, null=True)
    date_of_outcome = models.DateField(blank=True, null=True)      

    def __str__(self):           
        patient_name = self.patient_id.full_name if self.patient_id else "Unknown Patient"
        return f"{patient_name} ({self.id})"      