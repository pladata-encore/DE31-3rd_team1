from django.urls import path
from .views import chart_view
from . import views



urlpatterns = [
    path('', views.chart_view, name='chart'),  # /chart/ 경로에 대응하는 뷰 설정
]



app_name = 'chart'  # app_name 설정

