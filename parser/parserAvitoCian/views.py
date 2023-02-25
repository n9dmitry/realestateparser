import django
django.setup()
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.views.decorators.csrf import csrf_exempt

def all_Advertisment(request):
    adds = Advertisement.objects.all()

    return render(request, 'parserAvitoCian/index.html', 
        {
        'all_Advertisment':adds
        }
    )

@csrf_exempt
def request_proceed(request):
    adv_item = Advertisement(
        date=request.POST['date'],
        phone=request.POST['phone'],
        url=request.POST['url'],
        title=request.POST['title'],
        price=request.POST['price'],
        appartment_square=request.POST['appartment_square'],
        appartment_floor=request.POST['appartment_floor'],
        floors_count=request.POST['floors_count'],
        marketing_source=request.POST['marketing_source'],
    )
    adv_item.save()
    return HttpResponse('...')
