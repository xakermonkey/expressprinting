
from .views import *
from django.urls import path


urlpatterns = [
    path("<str:slug>", operatorForm, name='operator'),
    path("<str:slug>/get_order", get_order, name='get_order'),
    path("<str:slug>/orderdetails/<str:date>/printing", printing, name='printing'),
    path("<str:slug>/orderdetails/<str:date>/<str:num>", orderDetails, name='orderdetails'),
    path("<str:slug>/success_print", success_print, name='success'),

]
