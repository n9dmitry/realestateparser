import django
django.setup()
from django.http import HttpResponse
from django.shortcuts import render
from .models import *
from django.shortcuts import redirect
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
    print(request.POST)
    if request.method == 'POST':
        source_item = Source.objects.get(id=int(request.POST['marketing_source']))
        if not Advertisement.objects.filter(title=request.POST['title'], price=request.POST['price']).exists():
            adv_item = Advertisement(
                date=request.POST['date'],
                phone=request.POST['phone'],
                url=request.POST['url'],
                title=request.POST['title'],
                price=request.POST['price'],
                marketing_source=source_item,
            )

            adv_item.save()

        return redirect('all_adds')


