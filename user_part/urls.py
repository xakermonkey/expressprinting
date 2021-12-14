from .views import *
from django.urls import path


urlpatterns = [
    path("user", userForm, name='user'),
]
