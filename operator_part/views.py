import subprocess
from django.shortcuts import render
from .models import *
from django.http import JsonResponse
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

def operatorForm(request, pk):
    pos = POS.objects.get(id=pk)

    return render(request, 'operator_form.html', {'pos': pos})

def orderDetails(request, pk, date, num):
    order = Order.objects.get(pos=POS.objects.get(pk=pk),
                              date_create=datetime(day=int(date.split("-")[0]),
                                                   month=int(date.split("-")[1]),
                                                   year=int(date.split("-")[2])),
                              number=num)
    return render(request, 'order_details.html', {'order': order})



def success_print(request):
    order = Order.objects.get(id=request.POST.get('id'))
    order.date_print = datetime.today()
    order.save()
    return JsonResponse({'ok':'ok'})


def get_order(request):
    order = Order.objects.filter(number=request.POST.get('num'), date_create=datetime.today(), date_print=None).first()
    if order:
        return JsonResponse({'num': order.number,'date': datetime.today().strftime("%d-%m-%Y")})
    else:
        return JsonResponse({'num': '-'})

def printing(request, pk, date):
    order = Order.objects.get(id=request.POST.get('id'))
    for i in order.documents.all():
        for j in range(i.copy):
            text = f'lp -d {order.pos.name_printer} '
            text += ("\"/home/a_simakov/expressprinting/" + i.file.name + "\"")
            # logger.info(text)
            # text = 'ls'
            # print(text)
            # out = subprocess.run(text, shell=True)
            # print(out.stdout)
            # logger.info(out.stdout)
            # subprocess.run(text, stdout=subprocess.PIPE, universal_newlines=True)
    return JsonResponse({'ok': 'ok'})




