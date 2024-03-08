import json

import stripe
from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.views.generic.base import TemplateView

from basket.basket import Basket
from orders.views import payment_confirmation


"""
For payment system, we are using 'stripe'.
"""


@login_required
def BasketView(request):
    
    """
    Q: What's going on 'total'? And why there is basket?
    A: We are going to use 'stripe' as our payment system. 'stripe' gets value of purchase amount
       as integer type, for example $10.99 as 1099, so we need to convert it since our price is
       decimal. And reason we make 'Basket' instance by putting user's request, which sent to the 
       server as 'checkout'(pay) button is clicked inside of 'basket' page, is to get session 
       information from that user who clicked 'checkout' button.
    """
    basket = Basket(request)
    total = str(basket.get_total_price())
    total = total.replace('.','')
    total = int(total)

    # To sent 'stripe' api a request we need 'key' that is sent to the 'stripe' server to identify
    # our request. This key acutally need to be secret key
    stripe.api_key = 'pk_test_51KVDbjHKmi92LSUpXjyot87frrwM5FLOCyXr8fVgaKUR0gb3P6r5xGeXRRij71yoMd6HYoH7gBrKv7Nh58ZBWvRg00NgDe4A5a'

    # We need 'intent' since 'stripe' require it. In general intent exist to process user's action
    intent = stripe.PaymentIntent.create(
        
        # Amount of money user purchasing 
        amount=total,

        currency='gbp',
        
        # Send user's id who reqeust purchase to our server, to 'stripe' server. By sending user's id,
        # we can later retrieve id again from 'stripe' and match it with the user id of the order. So
        # we can check whether user's purchase of the order is done clearly.
        metadata={'userid':request.user.id}

    )

    # We get return from server of 'stripe' at this period, and able to retrieve 'client key'. 
    # 'client_secret' is made by 'stripe'
    return render(request, 'payment/home.html',{'client_secret':intent.client_secret})

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(json.loads(payload), stripe.api_key)
    except ValueError as e:
        print(e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        
        # Updating 'Order' data-table by this code.
        payment_confirmation(event.data.object.client_secret)

    else:
        print('Unhandled event type {}'.format(event.type))

    return HttpResponse(status=200)

def order_placed(request):
    basket = Basket(request)
    basket.clear()
    return render(request, 'payment/orderplaced.html')