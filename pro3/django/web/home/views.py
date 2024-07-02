from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
import os


def index(request):
    #return HttpResponse("첫 화면이 될 페이지")
    return render(request, 'home/index.html')

def get_wordcloud_image(request):
    date = request.GET.get('input-date')
    if date:
        image_path = os.path.join('static/images', f'{date}.png')
        if os.path.exists(image_path):
            image_url = f'/static/images/{date}.png'
        else:
            image_url = '/static/images/basic.png'
    else:
        image_url = '/static/images/basic.png'

    return JsonResponse({'image_url': image_url})