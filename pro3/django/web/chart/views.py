from django.shortcuts import render
import MySQLdb
from django.http import JsonResponse
import json

import matplotlib.pyplot as plt
from io import BytesIO
from django.http import HttpResponse
from .models import Test

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
    return render(request, 'chart/chart.html', context)


