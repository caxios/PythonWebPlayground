from django.db import models
from django.contrib.auth.models import User


# When database is created, data table would named as : "(app folder's name)_(model's name)"


class Category(models.Model):
    name = models.CharField(max_length=250, db_index=True)
    
    # 'Slug' is a string that can only include characters, numbers, dashes, and underscores. 
    # It is the part of a URL that identifies a particular page on a website, 
    # in a human-friendly form
    slug = models.SlugField(max_length=250, unique=True)

    class Meta:
        """
        'verbose_name' = A human-readable name for the object, singular
        'verbose_name_plural' = The plural name for the object. Djano would automatically pus -s 
        at the end of model name if this attribute is not specified. 
        """
        verbose_name_plural = 'categories'

    
    def __str__(self):
        """
        Q: Why use __str__?
        A: to display an object in the Django admin site and as the value inserted into
           a template when it displays an object
        """
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(Category, related_name='product', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='product_creator', on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=255, default='admin')
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=255)
    price = models.DecimalField(max_digits=4, decimal_places=2)
    in_stock = models.BooleanField(default=True)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Products'
        ordering = ('-created',)

    def __str__(self):
        return self.title