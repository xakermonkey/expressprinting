from .views import *
from django.urls import path


urlpatterns = [
    path("operator", operatorForm, name='operator'),
    path("orderdetails", orderDetails, name='orderdetails'),
]
