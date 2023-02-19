from django.shortcuts import render
from models import *

def all_Advertisment(request):
    adds = Advertisement.objects.all()
    return render(request, '')
