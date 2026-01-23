# models.py (Django backend updated for full patient data model)
import uuid   
from django.db import models
from patients.models import PatientCase

class Facility(models.Model):
    patient_id =  models.ForeignKey(    
        PatientCase,
        on_delete=models.SET_NULL,    
        null=True,            
        related_name='facility'  # <-- unique reverse name    
    )  
    designation = models.CharField(max_length=100)
    date_reported = models.DateField()
    form_completed_by = models.CharField(max_length=200)      
    health_facility_code = models.CharField(max_length=50)  
    case_source = models.CharField(max_length=70)     
    reporting_method = models.CharField(max_length=70)    
  
    def __str__(self):    
        return f"{self.full_name} ({self.patient_id})"                      
                                               