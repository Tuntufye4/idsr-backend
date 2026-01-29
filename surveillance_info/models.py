# models.py (Django backend updated for full patient data model)
import uuid   
from django.db import models
from patients.models import PatientCase

class SurveillanceInfo(models.Model):
    patient_id =  models.ForeignKey(    
        PatientCase,
        on_delete=models.SET_NULL,    
        null=True,            
        related_name='surveillance_info'  # <-- unique reverse name       
    )    
    reporting_week_number = models.IntegerField(null=True)      
    year = models.IntegerField(null=True)   
    date_reported = models.DateField(blank=True, null=True)    
    notifier_signature = models.CharField(max_length=100, blank=True, null=True) 
    reviewed_by = models.CharField(max_length=100, blank=True, null=True)     
    supervisor_comments = models.CharField(max_length=100, blank=True, null=True)  

    def __str__(self):    
        patient_name = self.patient_id.full_name if self.patient_id else "Unknown Patient"
        return f"{patient_name} ({self.id})"        
                                          