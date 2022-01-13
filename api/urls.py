from django.urls import path
from .views import *

urlpatterns = [
    path('create_pos', CreatePOS.as_view()),
    path('create_rates', CreateRates.as_view()),
    path('orders/<int:pk>', ShowOrders.as_view())
]
