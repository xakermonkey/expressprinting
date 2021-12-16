from .views import *
from django.urls import path


urlpatterns = [
    path("<int:pk>", operatorForm, name='operator'),
    path("<int:pk>/orderdetails/<str:date>/<int:num>", orderDetails, name='orderdetails'),
]
