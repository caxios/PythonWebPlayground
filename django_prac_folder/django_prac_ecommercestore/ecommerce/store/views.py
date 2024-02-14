from django.shortcuts import render
from .models import Product, Category


def product_all(request):
    products = Product.objects.all()
    return render(request, 'store/home.html', {'products':products})