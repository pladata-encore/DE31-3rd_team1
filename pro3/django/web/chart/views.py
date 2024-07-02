from django.shortcuts import render
from .models import Test

def chart_view(request):
    # counts가 가장 큰 15개의 keyword를 가져옴
    data = Test.objects.order_by('-count')[:15]
    
    keywords = [item.keywords for item in data]
    counts = [item.count for item in data]

    # 1위부터 15위까지 나열할 데이터 생성
    top_keywords = list(zip(keywords, counts))

    context = {
        'keywords': keywords,
        'counts': counts,
        'top_keywords': top_keywords,  # top_keywords를 컨텍스트에 추가
    }

    return render(request, 'chart/chart.html', context)
