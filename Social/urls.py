from django.urls import path
from django.contrib.auth import views as auth_views, authenticate

from . import views
from .forms import LoginForm

app_name = 'Social'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]