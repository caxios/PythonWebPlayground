from . import views
from django.urls import path

# define the application namespace for URL names defined within store/urls.py.
app_name='store'

urlpatterns = [
    path('', views.product_all, name='product_all'),
]