"""
This file is created to handle session for basket. Ecommerce basket store what user selected.
And in order for website to remeber what products were stored in basket, it needs to utilze
session. Session is simply user information that is saved in server. Why save it? Because in 
that way, website can provide some kind of personal(?) experience to its user.

So, instead of create a model that is holding and handling 'Product' object that user wants to 
temporarly add to basket, this file exists to use exisiting session data-table to store 
'Product' objects in the session of each user. So 'Basket' session holds data of 'Product' object.
And this session data is kept, and processed at server-side, unless we use ajax to show result of
session-update immediately to front-end(this doesn't mean session is updated at front-end, using
ajax just show the result when server finished session-update).

Since it is not a model, if cookie of browser deleted, then session also get deleted. So unlike
'Product' objects still exist(since they are made with model, and have its own data-table at data
base), 'basket' sesssion would be deleted.
"""

from store.models import Product
from decimal import Decimal
from django.conf import settings

class Basket:
    """
    A base Basket class, providing some default behaviors that
    can be inherited or overrided, as necessary.
    """
    
    """
    def __init__(self, request):
    self.session = request.session
    basket = self.session.get(settings.BASKET_SESSION_ID)
    if settings.BASKET_SESSION_ID not in request.session:
        basket = self.session[settings.BASKET_SESSION_ID] = {}
    self.basket = basket
    """
    def __init__(self, request):
        """
        Q: Why use '__init__'?
        A: To initialize some default value when 'Basket' object is instantiated. Values in __init__
           method can always be changed, since they are just initial value of 'Basket' instance.

        'self.session' = store 'request.session'. By this variable, instance of 'Basket' can access to
        session for user who sent that request.
        'basket' = It is also variable for 'Basket' instance. This is the one who actually holds
        session information of user for his/her basket. 
        """

        # Getting session from user's request
        self.session = request.session

        # skey : session-key
        basket = self.session.get('skey')
        
        if 'skey' not in request.session:
            
            # If the user who sent request have never made session
            # then, make session for user in session data-table.
            # And what this code doing is automatically save 'number' key and its value in
            # session data-table. So this code eventually store
            # {'skey':{'number':123123}} in session_data in session data-table.
            # basket = self.session['skey'] = {'number':123123}
            basket = self.session['skey'] = {}
        
        # Now allocate initial value for 'basket' variable
        self.basket = basket

    def add(self, product, product_qty):
        """
        Adding and updating the users basket session data
        """

        # Get specific product
        product_id = str(product.id)

        # Check whether product is already in basket or not 
        if product_id not in self.basket:
            
            # If product, which user is try to add basket, really doesn't exist in basket session
            # then, add product_id, and price information to session(basket). Eventually this would
            # be saved in session as : {'product_id':{'price':product.price, 'qty':product_qty}}
            self.basket[product_id] = {'price':str(product.price), 'qty':int(product_qty)}


        # Explicitly telling django session is updated. In this case, session is updated since,
        # we are adding product to basket.
        self.session.modified = True


    def __iter__(self):
        """
        Collect the product_id in the session data to query the database
        and return products

        
        Q: Why use '__iter__'?
        A: Since we cannot just retrieve all data objects from session, we need to first access to
           data-table of session and get 'Product' objects that we added to 'basket' session. 

           
        'product_ids' = We know 'session_data' column of 'basket' session data-table have all data 
        of 'Product' objects user have added to basket. Since 'basket' session is originaly of form 
        {'skey':{'product_id':{'price':product.price, 'qty':product_qty}}} and since 'self.basket' is
        of form : {'product_id':{'price':product.price, 'qty':product_qty}}, which is dictionary, we 
        can get its keys, which is 'product_id' of 'Product' objects that is added to the 
        'basket' sesseion. So if there is two different products in 'basket' session, then it would :
        {'skey':{'1':{'price':44.9, 'qty':4}},{'2':{'price':15.9, 'qty':1}},}
        
        'basket' = This allows modifications to be made to the copy without affecting the original 
        'self.basket' dictionary. It's crucial because we are not intending to alter the session 
        data directly during the iteration. We are just augmenting 'basket' temporarily for the 
        purpose of iteration to display the items in a template.
        """
        
        # Storing list of 'product_id' of 'Product' objects
        product_ids = self.basket.keys()
        
        products = Product.products.filter(id__in=product_ids)
        
        # Shallow copy of original 'self.basket'
        basket = self.basket.copy()

        for product in products:
            
            # This code would generate this in 'session_data' of 'basket' session data-table:
            # {'skey':{'product_id':{'price':product.price, 'qty':product_qty, 'product':product}}}
            basket[str(product.id)]['product'] = product

        # Copy version of 'basket' will be used.
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            
            # 'yield' returns generator. It means 'yield' returns value of iterable one by one
            # unlike 'return' returns value of iterable at one time. 
            yield item

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """

        # 'self.basket.values()' return all {'product_id':{'price':product.price, 'qty':product_qty}}
        # which are stored in column named 'session_data' of session data-table.
        return sum(item['qty'] for item in self.basket.values())

    def get_total_price(self):
        # return sum(item['total_price'] for item in self.basket.values())
        return sum(Decimal(item['price']) * item['qty'] for item in self.basket.values())
    
    def delete(self, product_id):
        """
        Delete item from session_data
        """

        # 'product_id' that we getting from parameter is integer type. And, under if-statement, we
        # try to access 'product' that we want to delete with 'product_id' key. But since 'product_id'
        # is string type, we need to change type. Otherwise, we still able to get value of 'product_id'
        # we cannot retrieve any value since type is mismatch.
        product_id = str(product_id)

        if product_id in self.basket:
            del self.basket[product_id]
            
        self.save()
    
    def update(self, product_id, product_qty):
        """
        Update values in session data
        """
        product_id = str(product_id)

        if product_id in self.basket:
            self.basket[product_id]['qty'] = int(product_qty)
        
        self.save()

    def save(self):
        self.session.modified = True

    """
    def clear(self):
        # Remove basket from session
        del self.session[settings.BASKET_SESSION_ID]
        self.save()
    """
    def clear(self):
        
        # Remove basket from session
        del self.session['skey']
        
        self.save()