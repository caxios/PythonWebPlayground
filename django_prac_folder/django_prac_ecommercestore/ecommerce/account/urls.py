from . import views
from .forms import (UserLoginForm)

from django.urls import path, reverse
from django.contrib.auth import views as auth_views

app_name='account'

urlpatterns = [
    path('register/', views.account_register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit', views.edit_details, name='edit_details'),
    
    # There are 2 url parameters, since we are passing 2 url parameters from 
    # 'account_activation_email.html'.
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
    
    # We are using django's pre-built views for login/out. And we don't need template for
    # logout, since we are just redirecting user to login page.
    path('login/', auth_views.LoginView.as_view(template_name='account/registration/login.html',
                                                form_class=UserLoginForm), name='login'),
    path('', auth_views.LogoutView.as_view(next_page='account/login'), name='logout'),
]