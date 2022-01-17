from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import *
from datetime import datetime
import os
import subprocess
from operator_part.cups_connection import set_connection_cups


def doc_to_pdf(path):
    doc = path[len(path) - 4:]
    docx = path[len(path) - 5:]
    rtf = path[len(path) - 4:]
    convert = f'soffice --headless --convert-to pdf '
    if doc == '.doc':
        convert += ("\"/opt/expressprinting/" + path + "\"")
        convert += (" --outdir \"" + "/".join(path.split('/')[:-1]) + "\"")
        logger.info(convert)
        out = subprocess.run(convert, shell=True)
        logger.info(out.stdout)
        pdf_path = path[:len(path) - 4] + ".pdf"
        logger.info(pdf_path)
        return pdf_path
    if docx == '.docx':
        convert += ("\"/opt/expressprinting/" + path + "\"")
        convert += (" --outdir \"" + "/".join(path.split('/')[:-1]) + "\"")
        logger.info(convert)
        out = subprocess.run(convert, shell=True)
        logger.info(out.stdout)
        pdf_path = path[:len(path) - 5] + ".pdf"
        logger.info(pdf_path)
        return pdf_path
    if rtf == '.rtf':
        convert += ("\"/opt/expressprinting/" + path + "\"")
        convert += (" --outdir \"" + "/".join(path.split('/')[:-1]) + "\"")
        logger.info(convert)
        out = subprocess.run(convert, shell=True)
        logger.info(out.stdout)
        pdf_path = path[:len(path) - 4] + ".pdf"
        logger.info(pdf_path)
        return pdf_path

def read_heandler(f, date):
    if not date.strftime("%d-%m-%Y") in os.listdir("templates/static/staff_file/"):
        os.mkdir(f'templates/static/staff_file/{date.strftime("%d-%m-%Y")}')
    with open(f'templates/static/staff_file/{date.strftime("%d-%m-%Y")}/{f.name}', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return f'templates/static/staff_file/{date.strftime("%d-%m-%Y")}/{f.name}'


class CreatePOS(APIView):

    def get(self, request):
        pos = POS.objects.all()
        serializer = SerializerPOS(pos, many=True)
        return Response(serializer.data)

    def post(self, request):
        pos = SerializerPOS(data=request.data)
        if pos.is_valid():
            pos.save()
            return Response(status=201)


class CreateRates(APIView):

    def get(self, request):
        rate = Rates.objects.all()
        serialzer = SerializerRate(rate, many=True)
        return Response(serialzer.data)

    def post(self, request):
        rate = SerializerRate(data=request.data)
        if rate.is_valid():
            rate.save()
            return Response(status=201)


class ShowOrders(APIView):

    def get(self, request, pk):
        orders = Order.objects.filter(pos=POS.objects.get(id=pk))
        serializer = SerializerOrders(orders, many=True)
        return Response(serializer.data)


class ShowStaffOrders(APIView):

    def get(self, request, pk):
        orders = StaffOrder.objects.filter(pos=POS.objects.get(id=pk))
        serializer = SerializerStaffWork(orders, many=True)
        return Response(serializer.data)



class staffPrinting(APIView):

    def post(self, request, slug):
        pos = POS.objects.get(slug=slug)
        work = StaffOrder.objects.create(pos=pos,
                                         date_print=datetime.today())
        for i in request.FILES:
            doc = Doc.objects.create(copy=1)
            path = read_heandler(request.FILES.get(i), work.date_print)
            doc.file.name = path[:len(path) - 4] + ".pdf"
            doc.name = path.split('/')[-1]
            doc.stati_path = "/".join(path.split('/')[2:])
            doc.save()
            if path.split('.')[-1] == 'doc' or path.split('.')[-1] == 'docx' or path.split('.')[-1] == 'rtf':
                doc_to_pdf(path)
            work.documents.add(doc)
        work.save()
        con = set_connection_cups()
        for i in work.documents.all():
            con.printFile(pos.name_printer, f"./{i.file.name}", "Express Print", {})
            # text = f'lp -d {work.pos.name_printer} '
            # text += ("\"/opt/expressprinting/" + i.file.name + "\"")
            # logger.info(text)
            # out = subprocess.run(text, shell=True)
            # logger.info(out.stdout)
        return Response(status=200, data={'status':True})
