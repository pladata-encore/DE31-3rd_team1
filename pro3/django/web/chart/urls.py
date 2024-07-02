from django.urls import path
from . import views

urlpatterns = [
    path('', views.chart_view, name='chart_view'),  # /chart/ 경로에 대응하는 뷰 설정
]
