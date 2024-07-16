from django.shortcuts import render
import os
import json
from django.db import connections
'''
def chart_view(request):
    date = request.GET.get('input-date')
    print(f"Received date from request: {date}")  # 디버깅 로그 추가
    for key, value in request.GET.items():
        print(f"{key}: {value}")
    
    if date:
        table_name = f"`{date}`"
    else:
        table_name = '`2024-07-01`'  # 기본값 설정

    # 동적으로 테이블 이름을 설정하여 데이터 가져오기
    with connections['default'].cursor() as cursor:
        cursor.execute(f"SELECT Keyword, count FROM {table_name} ORDER BY Count DESC LIMIT 15")
        rows = cursor.fetchall()

    Keyword = [row[0] for row in rows]
    count = [row[1] for row in rows]

    # top_keywords 리스트 생성
    top_keywords = list(zip(Keyword, count))

    print(f"Date: {date}, Table: {table_name}, Keyword: {Keyword}, count: {count}")  # 디버깅 로그 추가

    # top_keywords를 컨텍스트에 추가
    context = {
        'Keyword': json.dumps(Keyword),
        'count': json.dumps(count),
        'top_keywords': top_keywords,  # 이 줄을 추가하여 top_keywords를 템플릿에 전달
    }
    return render(request, 'chart/chart.html', context)

'''
from django.db import models

class Test1(models.Model):
    Keyword = models.TextField(db_column='Keyword', blank=True, primary_key=True)
    count = models.BigIntegerField(db_column='count', blank=True, null=True)

    class Meta:
        managed = False
        db_table = None  # 테이블 이름을 나중에 동적으로 설정

