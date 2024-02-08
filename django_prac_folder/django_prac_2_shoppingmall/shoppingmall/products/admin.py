from django.contrib import admin
from .models import Product

class ProductAdmin(admin.ModelAdmin):
    list_display = ("id","name","price","is_published","created_at")
    list_display_links = ("id","name")
    list_filter = ("price","name")
    list_editable = ("is_published",)
    search_fields = ("name","price")

# Register your models here.
admin.site.register(Product, ProductAdmin)