from django.urls import path
from .views import OtherView

urlpatterns = [
    path('', OtherView.as_view(), name='other'),
]