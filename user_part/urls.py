from .views import *
from django.urls import path


urlpatterns = [
    path("<int:pk>", userForm, name='user'),
    path('create_order', create_order, name="create_order"),
    # path('create_order', create_order, name="create_order"),
    path('<int:pk>/success_create/<int:pk_order>', success_create, name='success')
]
