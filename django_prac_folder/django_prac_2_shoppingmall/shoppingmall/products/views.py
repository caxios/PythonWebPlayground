from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Product, Comment
from .forms import productForm, commentForm
from datetime import datetime


# Create your views here.
def showProducts(request):
    # products = Product.objects.filter(is_published=True).order_by("price")
    # products_number = Product.objects.all().count()
    products = Product.objects.all()

    page_num = request.GET.get("page") # page number
    paginator = Paginator(products, 2) # which and how many to show

    try:
        products = paginator.page(page_num)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {"products":products}

    return render(request, "showProducts.html", context=context)

def showDetail(request, pk):
    product = Product.objects.get(pk=pk) # return single object
    context = {"product":product}

    return render(request, "productDetail.html", context=context)

def addProduct(request):
    form = productForm()

    if request.method == "POST":
        form = productForm(request.POST, request.FILES) #  request.FILES is needed since this dealing image file.
        if form.is_valid():
            form.save()
            return redirect('showProducts')

    context = {"form":form}

    return render(request, "addProduct.html", context=context)

def updateProduct(request, pk):
    product = Product.objects.get(pk=pk) # get functoin return single object, whereas filter function return queryset(multiple objects)
    form = productForm(instance=product) # need to give instace, since we are dealing specific product object.

    if request.method == "POST":
        form = productForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('showProducts')

    context = {"form":form}

    return render(request, "updateProduct.html", context=context)

def deleteProduct(request, pk):
    product = Product.objects.get(pk=pk)
    product.delete()

    return redirect('showProducts')

def searchbar(request):
    if request.method == "GET":
        query = request.GET.get("query")

        if query:
            products = Product.objects.filter(price__contains=query) # __icontains makes rough search, search keyword is no need to be accurate
            context = {"products":products}
            return render(request, 'searchBar.html', context=context)
        else:
            print("No information to show")
            return render(request, 'searchbar.html', {})
        
def addComment(request, pk):
    product = Product.objects.get(pk=pk)
    form = commentForm()

    if request.method == "POST":
        form = commentForm(request.POST, instance=product)
        if form.is_valid():
            name = request.user.username
            body = form.cleaned_data['comment_body']
            c = Comment(product=product, commenter_name=name, comment_body=body, date_added=datetime.now())
            c.save()
            # form.save() doesn't save comment.
            return redirect('showProducts')
        else:
            print("form is invalid")
    else:
        form = commentForm()

    context = {'form':form}

    return render(request, 'addComment.html', context=context)

def deleteComment(request, pk):
    comment = Comment.objects.filter(product=pk).last() # return queryset, not single object
    product_pk = comment.product.pk
    comment.delete()
    return redirect("showProducts") # redirect(reverse('showProducts', args=[product_pk]))