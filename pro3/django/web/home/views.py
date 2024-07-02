from django.shortcuts import render
from django.http import JsonResponse
import os
import json
from .models import Test1

def index(request):
    # counts가 가장 큰 15개의 keyword를 가져옴
    data = Test1.objects.order_by('-count')[:15]
    keywords = [item.keywords for item in data]
    counts = [item.count for item in data]

    # 입력된 날짜에 따라 이미지 경로를 동적으로 설정
    date = request.GET.get('input-date')
    if date:
        image_path = os.path.join('static/images', f'{date}.png')
        if os.path.exists(image_path):
            image_url = f'/static/images/{date}.png'
        else:
            image_url = '/static/images/basic.png'
    else:
        image_url = '/static/images/basic.png'
    
    context = {
        'keywords': json.dumps(keywords),  # JSON 데이터를 템플릿으로 전달
        'counts': json.dumps(counts),      # JSON 데이터를 템플릿으로 전달
        'image_url': image_url             # 동적으로 설정된 이미지 경로를 템플릿으로 전달
    }
    return render(request, 'home/index.html', context)
