from django.shortcuts import render
import os
import json
from django.db import connections

def index(request):
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
        cursor.execute(f"SELECT Keywords, Count FROM {table_name} ORDER BY Count DESC LIMIT 15")
        rows = cursor.fetchall()

    keywords = [row[0] for row in rows]
    counts = [row[1] for row in rows]

    print(f"Date: {date}, Table: {table_name}, Keywords: {keywords}, Counts: {counts}")  # 디버깅 로그 추가

    # 입력된 날짜에 따라 이미지 경로를 동적으로 설정
    if date:
        image_path = os.path.join('static/images', f'{date}.png')
        if os.path.exists(image_path):
            image_url = f'/static/images/{date}.png'
            print(f"Image path exists: {image_path}")
        else:
            image_url = '/static/images/basic.png'
            print(f"Image path does not exist, using basic image: {image_path}")
    else:
        image_url = '/static/images/basic.png'
        print("No date provided, using basic image")

    context = {
        'keywords': json.dumps(keywords),
        'counts': json.dumps(counts),
        'image_url': image_url
    }
    return render(request, 'home/index.html', context)
