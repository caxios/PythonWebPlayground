"""
Like context_processors.py in store app's folder, this file also exists to make 'basket' as 
project-wide context variable in all templates.
"""

from .basket import Basket

def basket(request):
    
    # Since 'Basket' get parameter user's request in its __init__ method, we need to pass request.
    return {'basket':Basket(request)}