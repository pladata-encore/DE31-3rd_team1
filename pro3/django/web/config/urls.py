from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # home 앱의 URL 설정 포함
    path('chart/', include('chart.urls')),  # chart 앱의 URL 설정 포함
]
