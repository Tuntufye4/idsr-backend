# models.py (Django backend updated for full patient data model)
import uuid   
from django.db import models
from patients.models import PatientCase

class Treatment(models.Model):
    patient_id = models.ForeignKey(    
        PatientCase,
        on_delete=models.SET_NULL,    
        null=True,            
        related_name='treatment'  # <-- unique reverse name    
    )  
    treatment_given = models.CharField(max_length=100, blank=True, null=True)
    procedures_done = models.CharField(max_length=200, blank=True, null=True)
    follow_up_plan = models.CharField(max_length=200, blank=True, null=True)
    referral_facility = models.CharField(max_length=200, blank=True, null=True)   
   
    def __str__(self):    
        patient_name = self.patient_id.full_name if self.patient_id else "Unknown Patient"
        return f"{patient_name} ({self.id})"   
                                                   


                                                     