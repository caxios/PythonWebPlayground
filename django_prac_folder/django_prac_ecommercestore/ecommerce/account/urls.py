from . import views
from django.urls import path

# Define the application namespace for URL names defined within store/urls.py.
app_name='basket'

urlpatterns = [
    path('', views.vview, name='vview'),

]