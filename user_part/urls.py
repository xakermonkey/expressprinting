from .views import *
from django.urls import path


urlpatterns = [
    path("<str:slug>", userForm, name='user'),
    path('<str:slug>/create_order', create_order, name="create_order"),
    # path('create_order', create_order, name="create_order"),
    path('<str:slug>/success_create/<int:pk_order>', success_create, name='success')
]
