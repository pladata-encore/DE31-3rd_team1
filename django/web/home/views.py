from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from datetime import datetime,timedelta
from django.db import connection
from django.utils.safestring import mark_safe
import os
from .models import Test1
import json



def index(request):
    # 현재 날짜를 YYYY-MM-DD 형식으로 가져오기
    today = datetime.now().strftime('%Y-%m-%d')
    yesterday = (datetime.now() - timedelta(days=1)).strftime('%Y-%m-%d')
    table = yesterday.strip("'")
    
    query = f"SELECT Keyword FROM `{table}` LIMIT 5"
    
    #query = "SELECT Keyword, count FROM test ORDER BY count DESC LIMIT 5"
    
    try:
        with connection.cursor() as cursor:
            cursor.execute(query)
            rows = cursor.fetchall()

        
        Keyword = [row[0] for row in rows]
        
    except Exception as e:
        Keyword = []
        
        print(f"오류 발생: {e}")
        
    context = {
        'yesterday': yesterday,
        'Keyword':mark_safe(Keyword),
    }
    return render(request, 'home/index.html', context)








