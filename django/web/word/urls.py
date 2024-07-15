from django.urls import path
from .views import word
from . import views

app_name = 'word'
urlpatterns = [
    path('', views.word, name='word'),  # /wordcloud/ 경로에 대응하는 뷰 설정
]