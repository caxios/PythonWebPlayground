"""
We set 'categories' as a context that is available on all templates of this project.
To do that, we have added 'store.context_processors.categories', so django can realize
'categories' is context for all templates. 
This file exists to make it much clear that 'categories' is context for all templates.
"""

from .models import Category

def categories(request):
    return {'categories':Category.objects.all()}
