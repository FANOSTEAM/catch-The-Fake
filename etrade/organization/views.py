from django.shortcuts import render
from django.http import JsonResponse
from .models import *
# Create your views here.
def org(request,tin):
    dictionary=dict()
    try:
        org=Organization.objects.get(OwnerTIN=str(tin))
        dictionary['phone']=org.phone
        return JsonResponse(dictionary)
    except Exception:
        return JsonResponse(dictionary)