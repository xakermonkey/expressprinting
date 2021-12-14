from django.shortcuts import render
from operator_part.models import *

def userForm(request, pk):
    pos = POS.objects.get(id=pk)
    return render(request, 'user_form.html', {'pos': pos})


def create_order(request):
    print(request.POST, request.FILES)

