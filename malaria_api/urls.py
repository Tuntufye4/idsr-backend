from django.contrib import admin   
from django.conf import settings   
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cases/', include('patients.urls')), 
    path('api/clinical/', include('clinical.urls')),
    path('api/epidemiological/', include('epidemiological.urls')),        
    path('api/facility/', include('facility.urls')),
    path('api/lab/', include('lab.urls')),
    path('api/outcomes/', include('outcomes.urls')),   
    path('api/surveillance_info/', include('surveillance_info.urls')),
    path('api/treatment/', include('treatment.urls')),     
]     
        

#if settings.DEBUG:
 #   import debug_toolbar
 #   urlpatterns += [
 #       path('__debug__/', include(debug_toolbar.urls)),
 #   ]   