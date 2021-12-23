
from .views import *
from django.urls import path


urlpatterns = [
    path("<int:pk>", operatorForm, name='operator'),
    path("get_order", get_order, name='get_order'),
    path("<int:pk>/orderdetails/<str:date>/printing", printing, name='printing'),
    path("<int:pk>/orderdetails/<str:date>/<str:num>", orderDetails, name='orderdetails'),
    path("success_print", success_print, name='success'),

]