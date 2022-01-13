from rest_framework import serializers

from operator_part.models import *


class SerializerOrders(serializers.ModelSerializer):
    """Сериализатор заказов"""

    pos = serializers.SlugRelatedField(slug_field='name', read_only=True)

    class Meta:
        model = Order
        exclude = ('id', 'documents')


class SerializerPOS(serializers.ModelSerializer):

    class Meta:
        model = POS
        fields = '__all__'

class SerializerRate(serializers.ModelSerializer):
    pos = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Rates
        fields = '__all__'
