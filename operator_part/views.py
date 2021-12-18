from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from datetime import datetime

def operatorForm(request, pk):
    pos = POS.objects.get(id=pk)
    orders = Order.objects.filter(pos=pos, date_print=None)
    print(orders)
    return render(request, 'operator_form.html', {'orders': orders, 'pos':pos})

def orderDetails(request, pk, date, num):
    order = Order.objects.get(pos=POS.objects.get(pk=pk),
                              date_create=datetime(day=int(date.split("-")[0]),
                                                   month=int(date.split("-")[1]),
                                                   year=int(date.split("-")[2])),
                              number=num)
    return render(request, 'order_details.html', {'order': order})



def success_print(request, pk, date):
    order = Order.objects.get(id=request.POST.get('id'))
    order.date_print = datetime.today()
    order.save()
    return JsonResponse({'ok':'ok'})


def remove(request):
    order = Order.objects.get(id=request.POST.get('id'))
    order.delete()
    return JsonResponse({'ok': 'ok'})
