from .views import *
from django.urls import path


urlpatterns = [
    path("<int:pk>", operatorForm, name='operator'),
    path("remove", remove, name='remove'),
    path("<int:pk>/orderdetails/<str:date>/<int:num>", orderDetails, name='orderdetails'),
    path("<int:pk>/orderdetails/<str:date>/success_print", success_print, name='success'),
]
