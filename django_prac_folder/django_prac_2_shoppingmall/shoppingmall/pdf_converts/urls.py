from django.urls import path
from . import views

urlpatterns = [
    path('showproducts/',views.showProducts, name='pdfshowProducts'),
    path('converts/',views.pdf_report_create, name='create-pdf'),

]