import sys
from django.urls import resolve

def getCurrentHost(request):
    return request.META['HTTP_REFERER']

def get_app_name(request):
    return sys.modules[resolve(request.path_info).func.__module__].__package__