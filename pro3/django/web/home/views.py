from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import os
import MySQLdb
from django.http import JsonResponse
import json

import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse
from .models import Test

from django.shortcuts import render
import MySQLdb
from django.http import JsonResponse
import json

def index(request):
    #return HttpResponse("첫 화면이 될 페이지")
    return render(request, 'home/index.html')

def get_wordcloud_image(request):
    date = request.GET.get('input-date')
    if date:
        image_path = os.path.join('static/images', f'{date}.png')
        if os.path.exists(image_path):
            image_url = f'/static/images/{date}.png'
        else:
            image_url = '/static/images/basic.png'
    else:
        image_url = '/static/images/basic.png'

    return JsonResponse({'image_url': image_url})

from django.shortcuts import render


def chart_view(request):
    # counts가 가장 큰 15개의 keyword를 가져옴
    data = Test.objects.order_by('-count')[:15]
    # print('data :', data)  # 콘솔에 데이터를 출력하여 확인
    keywords = [item.keywords for item in data]
    counts = [item.count for item in data]
    # for item in data:
        # print(item.Keywords, item.Counts)  # 각 항목의 값을 출력하여 확인
    context = {
        'keywords': keywords,
        'counts': counts,
    }
    return render(request, 'home/index.html', context)
