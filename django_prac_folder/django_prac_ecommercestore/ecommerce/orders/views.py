from django.shortcuts import render
from django.http.response import JsonResponse

from basket.basket import Basket
from .models import Order, OrderItem

# Create your views here.
def add(request):
    basket = Basket(request)
    
    """
    Q: Why not just request.method == 'POST'?
    A: They slightly different. While above code checks whether user's request is POST or not,
       request.POST.get('action') == 'post' assumes user is requesting POST, but what action does
       user exactly want the server to handle. So we usually POST to adjust some data from client
       side, and send to server. Those types of adjustments includes update, delete, post etc. 
       If we want to seperate operations on those different types of adjustments, only checking 
       whether reqeust is POST or not is insufficient.  
    """
    if request.POST.get('action') == 'post':
        user_id = request.user.id
        order_key = request.POST.get('order_key') # This key is made by stripe. See 'index.js'
        baskettotal = basket.get_total_price()

        # Check if order exists
        if Order.objects.filter(order_key=order_key).exists():
            pass
        else:
            order = Order.objects.create(user_id=user_id, full_name='eee', address1='add1',
                                         address2='add2', total_paid=baskettotal, order_key=order_key)
            
            # Don't confuse 'order_id' with 'order_key', which is a variable that stores user's order
            # payment key made by stripe.  
            order_id = order.pk

            for item in basket:
                OrderItem.objects.create(order_id=order_id, product=item['product'],
                                         price=item['price'], quantity=item['qty'])  
        response = JsonResponse({'success': 'Return something'})
        return response

# This function is used in 'payment/veiws.py/stripe_webhook' to literally confirm payment,
# and change status if correctly processed purchase. 
def payment_confirmation(data):
    Order.objects.filter(order_key=data).update(billing_status=True)

def user_orders(request):
    user_id = request.user.id
    orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)
    return orders