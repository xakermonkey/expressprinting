from django.shortcuts import render
from operator_part.models import *
from django.http import JsonResponse
from datetime import datetime
import random
import PyPDF2
import os
from zipfile import ZipFile


def userForm(request, pk):
    pos = POS.objects.get(id=pk)
    tarif = Rates.objects.filter(pos=pos).order_by('date').last()
    return render(request, 'user_form.html', {'pos': pos, 'rate':tarif})


def success_create(request, pk, date, num):
    order = Order.objects.get(pos=POS.objects.get(pk=pk),
                              date_create=datetime(day=int(date.split("-")[0]),
                                                   month=int(date.split("-")[1]),
                                                   year=int(date.split("-")[2])),
                              number=num)
    return render(request, 'success_create.html', {'order': order, 'code':str(order.code)})


def pages_count(path):
    return PyPDF2.PdfFileReader(open(path, "rb")).numPages


def pages_count_word(path):
    z = ZipFile(path)
    text = str(z.read('docProps/app.xml'))
    page = text.find('<Pages>')
    end = text.find('</Pages>')
    return int(text[page + 7:end])


def read_heandler(f, date, num):
    if not date.strftime("%d-%m-%Y") in os.listdir("templates/static/orders/"):
        os.mkdir(f'templates/static/orders/{date.strftime("%d-%m-%Y")}')
        os.mkdir(f'templates/static/orders/{date.strftime("%d-%m-%Y")}/{num}/')
    elif not str(num) in os.listdir(f'templates/static/orders/{date.strftime("%d-%m-%Y")}/'):
        os.mkdir(f'templates/static/orders/{date.strftime("%d-%m-%Y")}/{num}/')
    with open(f'templates/static/orders/{date.strftime("%d-%m-%Y")}/{num}/{f.name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return f'templates/static/orders/{date.strftime("%d-%m-%Y")}/{num}/{f.name}'


def create_order(request):
    pos = POS.objects.get(id=request.POST.get('pos'))
    rate = Rates.objects.filter(pos=pos).order_by('date').last()
    order = Order.objects.create(pos=pos,
                                 date_create=datetime.today(),
                                 number=Order.objects.filter(date_create=datetime.today()).count() + 1,
                                 code=random.randint(999, 9999),
                                 price_per_list=rate.price_per_list
                                 )
    count_page = 0
    for i in request.FILES:
        copy = int(request.POST.get('copy' + i[4:]))
        doc = Doc.objects.create(copy=copy)
        path = read_heandler(request.FILES.get(i), order.date_create, order.number)
        doc.file.name = path
        doc.name = path.split('/')[-1]
        doc.stati_path = "/".join(path.split('/')[2:])
        doc.save()
        if path.split('.')[-1] == 'pdf':
            count_page += pages_count(path) * copy
        if path.split('.')[-1] == 'doc' or path.split('.')[-1] == 'docx' or path.split('.')[-1] == 'rtf':
            count_page += pages_count_word(path) * copy
        order.documents.add(doc)
    order.list_count = count_page
    order.amount = order.list_count * order.price_per_list
    order.save()
    return JsonResponse({'num': order.number, 'id':order.id, 'date': datetime.today().strftime("%d-%m-%Y"), 'code': order.code})