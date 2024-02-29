from . import views
from .forms import (PwdResetConfirmForm, PwdResetForm, UserLoginForm)

from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView

app_name='account'

# Consider '/main/menu'. When URL starts with '/' then, it means path starts from the root.
# When start without '/' 'main/menu' then, it just start from ../main. So it means
# The leading slash indicates that the path should be interpreted as an absolute path.
# But the absence of a leading slash denotes a relative path. This path is relative to the 
# current URL's path.
urlpatterns = [
    path('register/', views.account_register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/edit', views.edit_details, name='edit_details'),
    path('profile/delete_user', views.delete_user, name='delete_user'),
    path('profile/delete_confirmation', TemplateView.as_view(
        template_name='account/user/delete_confirmation.html'), name='delete_confirmation'),
    
    # There are 2 url parameters, since we are passing 2 url parameters from 
    # 'account_activation_email.html'.
    path('activate/<slug:uidb64>/<slug:token>/', views.account_activate, name='activate'),
    
    # We are using django's pre-built views for login/out. And we don't need template for
    # logout, since we are just redirecting user to login page.
    path('login/', auth_views.LoginView.as_view(
        template_name='account/registration/login.html',
        form_class=UserLoginForm), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/account/login'), name='logout'),

    path('password_reset/', auth_views.PasswordResetView.as_view(
        template_name="account/user/password_reset_form.html",
        success_url='password_reset_email_confirm',
        email_template_name='account/user/password_reset_email.html',
        form_class=PwdResetForm), name='pwdreset'),
    path('password_reset_confirm/<uidb64>/<token>', auth_views.PasswordResetConfirmView.as_view(
        template_name='account/user/password_reset_confirm.html',
        success_url='/account/password_reset_complete/', 
        form_class=PwdResetConfirmForm), name='password_reset_confirm'),
    path('password_reset/password_reset_email_confirm/', TemplateView.as_view(
        template_name="account/user/reset_status.html"), name='password_reset_done'),
]