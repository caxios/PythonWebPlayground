from . import views
from django.urls import path

app_name='account'

urlpatterns = [
    path('register/', views.account_register, name='register'),
    
    # There are 2 url parameters, since we are passing 2 url parameters from 
    # 'account_activation_email.html'.
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
    
    path('dashboard/', views.dashboard, name='dashboard'),
]