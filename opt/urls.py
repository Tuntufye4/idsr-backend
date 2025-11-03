from django.urls import path, include
from .views import get_form_options
   
urlpatterns = [
    path('form-options/', get_form_options, name='form-options'),
]
      