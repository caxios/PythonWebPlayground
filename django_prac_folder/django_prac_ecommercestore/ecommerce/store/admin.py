from django.contrib import admin
from .models import Category, Product

"""

"""
@admin.register(Category) # same as admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """

    The @admin.register(Category) decorator is a shorthand for registering a model (Category, in this 
    case) with the admin site, associating it with a custom admin class (CategoryAdmin). 
    This custom class defines how the model should be displayed and managed in the Django admin interface.

    When we use the @admin.register(Category) decorator, it does the following:
    1. It takes the model class Category as an argument.
    2. It then calls the register method of Django's default admin site instance, passing the Category 
    model and the CategoryAdmin class to it.
    3. This registration process tells Django's admin site that you want to use the CategoryAdmin 
    class to customize the admin interface for your Category model.
    
    ******************
    
    'list_display' = informations we want to display about model in admin site.
    'prepopulated_fields' = The main use for this functionality is to automatically 
    generate the value for SlugField fields from one or more other fields
    
    """
    list_display = ['name','slug']
    
    # 'prepopulated_fields' indicates that the slug field in the Category model will be automatically 
    # filled in with a URL-friendly version of whatever is entered into the name field, 
    # dynamically updating as the name field is typed into.
    prepopulated_fields = {'slug':('name',)}

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'slug', 'price', 'in_stock', 'created', 'updated', 'category', 'is_active']
    list_filter = ['in_stock', 'is_active']
    list_editable = ['price', 'in_stock', 'is_active']
    prepopulated_fields = {'slug': ('title',)}