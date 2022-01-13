from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from operator_part.models import *
from .serializers import *


# Create your views here.


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
