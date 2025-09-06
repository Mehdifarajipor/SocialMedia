from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout

from .forms import RegisterForm

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