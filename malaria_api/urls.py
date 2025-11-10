from django.contrib import admin
from django.conf import settings   
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('patients.urls')),
    path('api/', include('clinical.urls')),
    path('api/', include('epidemiological.urls')),     
    path('api/', include('facility.urls')),
    path('api/', include('lab.urls')),
    path('api/', include('outcomes.urls')),
    path('api/', include('surveillance_info.urls')),
    path('api/', include('treatment.urls')),  
    path('api/', include('opt.urls')),  
]     
        

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]   