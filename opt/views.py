import yaml
from pathlib import Path
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['GET'])
def get_form_options(request):
    """Return dropdown options from YAML file"""
    # Correct path when 'yaml' folder is in the same directory as views.py
    file_path = Path(__file__).resolve().parent / 'yaml' / 'form_options.yml'
    
    with open(file_path, 'r') as file:
        options = yaml.safe_load(file)
    
    return Response(options)
