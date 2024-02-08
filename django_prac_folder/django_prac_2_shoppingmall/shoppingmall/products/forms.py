from django import forms
from .models import Product

class productForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['image','name','price','is_published','description']
        widgets = {
            'image':forms.FileInput(attrs={"class":"form-control"}),
            'name':forms.TextInput(attrs={"class":"form-control"}),
            'price':forms.TextInput(attrs={"class":"form-control"}),
            'description':forms.TextInput(attrs={"class":"form-control"}),
        }