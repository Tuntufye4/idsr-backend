from django.contrib import admin
from .models import PatientCase

@admin.register(PatientCase)
class PatientCaseAdmin(admin.ModelAdmin):
    list_display = (
        "patient_id", "full_name", "health_facility", "district", "disease",
        "case_classification", "outcome", "date_reported"
    )
    search_fields = ("full_name", "patient_id", "district", "disease", "national_id")
    list_filter = ("district", "case_classification", "outcome", "year", "health_facility")
                            