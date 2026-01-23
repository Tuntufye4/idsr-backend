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
    reporting_week_number = models.IntegerField()      
    year = models.IntegerField()   
    date_reported = models.DateField()    
    notifier_signature = models.CharField(max_length=100, blank=True, null=True) 
    reviewed_by = models.CharField(max_length=100, blank=True, null=True)     
    supervisor_comments = models.CharField(max_length=100, blank=True, null=True)  

    def __str__(self):    
        return f"{self.full_name} ({self.patient_id})"        
                                          