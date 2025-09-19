from django.urls import path
from django.contrib.auth import views as auth_views, authenticate

from . import views
from .forms import LoginForm

app_name = 'Social'

urlpatterns = [
    path('', views.index, name='index'),
    path('posts/', views.post_list, name='post_list'),
    path('posts-by-tag/<slug:tag_slug>/', views.post_list, name='post_list_by_tag'),
    path('posts/<int:pk>/', views.post_detail, name='post_detail'),
    path('login/', auth_views.LoginView.as_view(authentication_form=LoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('user/edit/', views.user_edit, name='user_edit'),
    path('ticket/', views.ticket, name='ticket'),
    path('posts/create/', views.post_create, name='post_create'),

    path('password-reset/', auth_views.PasswordResetView.as_view(success_url='done'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView
         .as_view(success_url='/password-reset/complete/'), name='password_reset_confirm'),
    path('password-reset/complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

    path('password-change/', auth_views.PasswordChangeView.as_view(
        success_url='/password-change/done'), name='password_change'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(), name="password_change_done"),

    path('search/', views.post_search, name='post_search'),
    path('posts/<int:pk>/edit/', views.post_edit, name='post_edit'),
    path('posts/<int:pk>/delete/', views.post_delete, name='post_delete'),
    path('like-post/', views.like_post, name='like_post'),
    path('save-post/', views.save_post, name='save_post'),
    path('profile/', views.profile, name='profile'),
    path('user-list/', views.user_list, name='user_list'),
    path('user-detail/<username>/', views.user_detail, name='user_detail'),

]