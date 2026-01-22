# models.py (Django backend updated for full patient data model)
import uuid   
from django.db import models

class PatientCase(models.Model):
    patient_id = models.CharField(max_length=50, unique=True, editable=False, default=uuid.uuid4)
    full_name = models.CharField(max_length=200)
    age = models.IntegerField()    
    sex = models.CharField(max_length=10)      
    date_of_birth = models.DateField()         
    national_id = models.CharField(max_length=100, blank=True, null=True)    
    village = models.CharField(max_length=200)                                                
    traditional_authority = models.CharField(max_length=200)    
    district = models.CharField(max_length=200)   
    region = models.CharField(max_length=100)          

    def __str__(self):    
        return f"{self.full_name} ({self.patient_id})"        
                                              