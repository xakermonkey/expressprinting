from .views import *
from django.urls import path


urlpatterns = [
    path("<int:pk>", userForm, name='user'),
    path('create_order', create_order, name="create_order")
]
