from django.shortcuts import render
import MySQLdb
from django.http import JsonResponse
import json


def chart_view(request):
    '''
    db_config = {
        "host" : "43.202.5.70", 
        "user" : "class5",
        "password" : "EnCoRo!23",
        "database" : "encore_web" 
    }
    con = MySQLdb.connect(**db_config)
    cur = con.cursor()

    cur.execute("select * from result")
    data = cur.fetchall()
    cur.close()
    con.close()

    labels    = [x[0] for x in data]
    Cancelled = [x[1] for x in data]
    Divered   = [x[2] for x in data]
    Air       = [x[3] for x in data]

    datasets = [
        {'label' : 'Cancelled', 'data' : Cancelled, 'backgroundColor': 'rgba(255, 99, 132, 0.5)' },
        {'label' : 'Divered',   'data' : Divered,   'backgroundColor': 'rgba(54, 160, 235, 0.5)' },
        {'label' : 'Air',       'data' : Air,       'backgroundColor': 'rgba(75, 199, 192, 0.5)' },
    ]

    chart_data = {
        'labels' : labels,
        'datasets' : datasets
    }
    '''
    return render(request, 'chart/chart.html')


import matplotlib.pyplot as plt
from django.shortcuts import render
from io import BytesIO
from django.http import HttpResponse
from .models import SalesData

def sales_chart(request):
    sales_data = SalesData.objects.all().order_by('date')
    dates = [data.date for data in sales_data]
    sales = [data.sales for data in sales_data]

    plt.figure(figsize=(10, 5))
    plt.plot(dates, sales, marker='o')
    plt.title('Sales Over Time')
    plt.xlabel('Date')
    plt.ylabel('Sales')
    plt.grid(True)

    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    return HttpResponse(buffer, content_type='image/png')
