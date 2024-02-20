from django.shortcuts import render, get_object_or_404
from .basket import Basket
from store.models import Product
from django.http import Http404, JsonResponse

# Create your views here.
def basket_summary(request):
    return render(request, 'store/basket/summary.html')

def basket_add(request):
    """
    This view-function handles request from user.
    """
    
    # Make 'basket' instance. It is a session for user's basket
    basket = Basket(request)

    """
    Q: What is "request.POST.get('action')" and "request.POST.get('productid')"?
    A: Inside of  detail.html, we wrote jquery code. There, we had set
       type of request method we want to modifiy, and data we want to send with.
       .get() method allow us to find content inside of 'POST' request box. So 
       .get('action') is looking for data which key name is 'action, and .get('productid)
       id looking for data which key name is 'productid'.
    """
    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        
        # Below try-except statement can be shortten as : get_object_or_404(Product, id=product_id)
        try:
            product = Product.objects.get(id=product_id)
        except:
            raise Http404
        
        # Saving data of product and product quantity to basket.
        basket.add(product=product, product_qty=product_qty)

        # Save 'basket_qty' to 'response' variable as JsonResponse object, and send it back to
        # client. Client side can receive json value, since in detail.html we have set when
        # request is successfuly processed in server, and sending back response to cleint,
        # success would be triggered, and
        # success function would retrieve 'json' as its parameter.
        # If not, then error msg sent back, and error function is triggered.
        basket_qty = basket.__len__()
        response = JsonResponse({'qty':basket_qty})
        
        return response

def basket_delete(request):
    basket = Basket(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        basket.delete(product_id=product_id)
        
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()        
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response

def basket_update(request):
    basket = Basket(request)

    if request.POST.get('action') == 'post':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product_id=product_id, product_qty=product_qty)
        
        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response