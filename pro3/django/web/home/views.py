from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    #return HttpResponse("첫 화면이 될 페이지")
    return render(request, 'home/index.html')