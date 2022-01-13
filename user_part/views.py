from django.shortcuts import render
from operator_part.models import *
from django.http import JsonResponse
from datetime import datetime
import PyPDF2
import os
from zipfile import ZipFile


def userForm(request, slug):
    pos = POS.objects.get(slug=slug)
    tarif = Rates.objects.filter(pos=pos).order_by('date').last()
    return render(request, 'user_form.html', {'pos': pos, 'rate':tarif})


def success_create(request, slug, pk_order):
    order = Order.objects.get(id=pk_order)
    return render(request, 'success_create.html', {'order': order, 'code': str(order.number)})


def pages_count(path):
    return PyPDF2.PdfFileReader(open(path, "rb")).numPages


def doc_to_pdf(path):
    doc = path[len(path) - 4:]
    docx = path[len(path) - 5:]
    rtf = path[len(path) - 4:]
    convert = f'soffice --headless --convert-to pdf '
    if doc == '.doc':
        convert += ("\"/home/a_simakov/expressprinting/" + path + "\"")
        convert += (" --outdir \"" + "/".join(path.split('/')[:-1]) + "\"")
        logger.info(convert)
        out = subprocess.run(convert, shell=True)
        logger.info(out.stdout)
        pdf_path = path[:len(path) - 4] + ".pdf"
        logger.info(pdf_path)
        return pdf_path
    if docx == '.docx':
        convert += ("\"/home/a_simakov/expressprinting/" + path + "\"")
        convert += (" --outdir \"" + "/".join(path.split('/')[:-1]) + "\"")
        logger.info(convert)
        out = subprocess.run(convert, shell=True)
        logger.info(out.stdout)
        pdf_path = path[:len(path) - 5] + ".pdf"
        logger.info(pdf_path)
        return pdf_path
    if rtf == '.rtf':
        convert += ("\"/home/a_simakov/expressprinting/" + path + "\"")
        convert += (" --outdir \"" + "/".join(path.split('/')[:-1]) + "\"")
        logger.info(convert)
        out = subprocess.run(convert, shell=True)
        logger.info(out.stdout)
        pdf_path = path[:len(path) - 4] + ".pdf"
        logger.info(pdf_path)
        return pdf_path

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




def create_order(request, slug):
    pos = POS.objects.get(id=request.POST.get('pos'))
    rate = Rates.objects.filter(pos=pos).order_by('date').last()
    num = str(Order.objects.filter(date_create=datetime.today()).count() + 1)
    order = Order.objects.create(pos=pos,
                                 date_create=datetime.today(),
                                 number='0'*(3-len(num))+num,
                                 price_per_list=rate.price_per_list
                                 )
    count_page = 0
    for i in request.FILES:
        copy = int(request.POST.get('copy' + i[4:]))
        doc = Doc.objects.create(copy=copy)
        path = read_heandler(request.FILES.get(i), order.date_create, order.number)
        doc.file.name = path[:len(path) - 4] + ".pdf"
        doc.name = path.split('/')[-1]
        doc.stati_path = "/".join(path.split('/')[2:])
        doc.save()
        if path.split('.')[-1] == 'pdf':
            count_page += pages_count(path) * copy
        if path.split('.')[-1] == 'doc' or path.split('.')[-1] == 'docx' or path.split('.')[-1] == 'rtf':
            pdf_path = doc_to_pdf(path)
            count_page += pages_count(pdf_path) * copy
        order.documents.add(doc)
    order.list_count = count_page
    order.amount = order.list_count * order.price_per_list
    order.save()
    return JsonResponse({'id':order.id})
