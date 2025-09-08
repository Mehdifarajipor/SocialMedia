from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from .forms import *

# Create your views here.


def index(request):
    return render(request, 'Social/index.html')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            return render(request, 'registration/register_done.html')
    else:
        form = RegisterForm()
    return render(request, 'registration/register.html', {'form': form})


def user_edit(request):
    if request.method == 'POST':
        form = UserEditForm(instance=request.user, data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('Social:index')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'registration/edit_user.html', {'form': form})