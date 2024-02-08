from django.urls import path
from . import views

urlpatterns = [
    path('',views.showProducts, name='showProducts'),
    path('detail/<int:pk>',views.showDetail, name='showDetail'),
    path('addproduct/',views.addProduct, name='addProduct'),
    path('updateproduct/<int:pk>',views.updateProduct, name='updateProduct'),
    path('deleteproduct/<int:pk>',views.deleteProduct, name='deleteProduct'),
    path('searchBar/',views.searchbar, name='searchBar'),
]