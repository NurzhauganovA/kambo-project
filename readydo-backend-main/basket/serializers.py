from rest_framework import serializers

from auth_user.serializers import UserProfileSerializer
from basket.models import OrderItem, Order, OrderChoices
from foods.serializers import FoodSerializer


class AddToBasketSerializers(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['food', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    status_decode = serializers.SerializerMethodField()
    customer = UserProfileSerializer()

    class Meta:
        model = Order
        exclude = ['created_at', 'updated_at',]

    def get_status_decode(self, obj):
        return OrderChoices(obj.status).label


class BasketChangeStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['status']


class ChangeProductQuantitySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['quantity']


class BasketFoodsListSerializer(serializers.ModelSerializer):
    product_info = FoodSerializer(source='food')

    class Meta:
        model = OrderItem
        exclude = ['created_at', 'updated_at']
