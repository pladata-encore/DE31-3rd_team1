from django.shortcuts import render
import os
import json
from django.db import connections

def chart_view(request):
    date = request.GET.get('input-date')
    print(f"Received date from request: {date}")  
    for key, value in request.GET.items():
        print(f"{key}: {value}")
    
    if date:
        table_name = f"`{date}`"
    else:
        table_name = '`2024-07-01`'  # 기본값 설정

    with connections['default'].cursor() as cursor:
        cursor.execute(f"SELECT Keyword, count FROM {table_name} ORDER BY Count DESC LIMIT 15 OFFSET 15")
        rows = cursor.fetchall()

    Keyword = [row[0] for row in rows]
    count = [row[1] for row in rows]

    # top_Keyword 리스트 생성
    top_Keyword = list(zip(Keyword, count))

    print(f"Date: {date}, Table: {table_name}, Keyword: {Keyword}, count: {count}") 
    # top_Keyword를 컨텍스트에 추가
    context = {
        'Keyword': json.dumps(Keyword),
        'count': json.dumps(count),
        'top_Keyword': top_Keyword,  
        'table_name': table_name,
    }
    return render(request, 'chart/chart.html', context)