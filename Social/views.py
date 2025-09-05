from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

# Create your views here.


def index(request):
    return render(request, 'Social/index.html')