from django.db import models
from datetime import datetime

# Create your models here.
class Product(models.Model):
    image = models.ImageField(null=False, blank=False)
    name = models.CharField(max_length=200, null=False, blank=False)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField()
    is_published = models.BooleanField(default=True)
    created_at = models.DateField(default=datetime.now, blank=True)

    def __str__(self):
        return self.name
    
class Comment(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='comments')
    commenter_name = models.CharField(max_length=200)
    comment_body = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return '%s - %s' % (self.product.name, self.commenter_name)