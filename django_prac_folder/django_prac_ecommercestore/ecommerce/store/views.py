from django.shortcuts import get_object_or_404, render
from .models import Product, Category


def product_all(request):
    
    # this code is now act as Product.objects.filter(is_active=True), since we set 
    # 'ProductManager' for 'Product' model in models.py Since we set 'ProductManager' for 'Product'
    # model, now all 'Product' objects apply 'set_queryset'. But Product.objects.all() works as same.
    products = Product.products.all()
    
    return render(request, 'store/home.html', {'products':products})

def product_detail(request, slug):

    # get one item(object) from database(data-table) that matches 'slug' with that is inside
    # of user's request. If no matches, then return 404 error.
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    
    return render(request, 'store/products/detail.html', {'product': product})

def category_list(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug) # Category.objects.get(slug=category_slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category':category, 'products': products})