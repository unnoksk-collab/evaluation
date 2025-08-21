from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    # Django標準のログイン・ログアウト機能を利用
    path('login/', auth_views.LoginView.as_view(template_name='ranking/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]