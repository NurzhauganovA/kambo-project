from django.shortcuts import render
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.exceptions import ValidationError, NotFound, PermissionDenied
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from basket.models import OrderItem, OrderChoices, Order
from basket.serializers import AddToBasketSerializers, OrderSerializer, BasketChangeStatusSerializer, \
    ChangeProductQuantitySerializer, BasketFoodsListSerializer
from basket.services import get_or_create_pending_basket, update_basket_total_price
from common.manual_parameters import QUERY_BASKET_STATUS
from foods.models import Food


class AddToBasketAPIView(generics.CreateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = AddToBasketSerializers
    parser_classes = (MultiPartParser,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        food = serializer.validated_data['food']
        quantity = serializer.validated_data['quantity']

        user = self.request.user

        if food:
            pending_user_basket = get_or_create_pending_basket(user).first()
            update_order_item = OrderItem.objects.filter(order=pending_user_basket.id, food=food).first()

            if update_order_item:
                basket_old_quantity = update_order_item.quantity
                update_order_item.quantity = basket_old_quantity+quantity
                update_order_item.save(update_fields=['quantity'])
                update_basket_total_price(pending_user_basket)
                return Response({'message': 'Вы успешно обнавили каличество товара'}, status=status.HTTP_200_OK)
            else:
                OrderItem.objects.create(order=pending_user_basket, food=food, quantity=quantity)
                update_basket_total_price(pending_user_basket)
                return Response({'message': 'Вы успешно добавили товар в карзину'}, status=status.HTTP_201_CREATED)
        else:
            return Response({"message": "Такого товара не существует"}, status=status.HTTP_404_NOT_FOUND)


class BasketUserListAPIView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = OrderSerializer
    parser_classes = (MultiPartParser,)

    def get_queryset(self):
        basket_status = self.request.query_params.get('status')
        user = self.request.user

        if user.is_superuser and (basket_status is None):
            return Order.objects.all()
        if basket_status:
            valid_statuses = [choice[0] for choice in OrderChoices.choices]
            if int(basket_status) not in valid_statuses:
                raise ValidationError("Недопустимый статус корзины.")

            return Order.objects.filter(customer=user, status=basket_status)
        return Order.objects.filter(customer=user)

    @swagger_auto_schema(manual_parameters=[QUERY_BASKET_STATUS])
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class BasketChangeStatusAPIView(generics.UpdateAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)
    serializer_class = BasketChangeStatusSerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            if user.is_superuser:
                return Order.objects.all()
            return Order.objects.filter(customer=user)

    def update(self, request, *args, **kwargs):
        status = self.get_object()
        serializer = self.get_serializer(status, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class RemoveBasketAPIView(generics.DestroyAPIView):
    permission_classes = (IsAuthenticated,)
    parser_classes = (MultiPartParser,)
    queryset = OrderItem.objects.all()

    def get_object(self):
        user = self.request.user
        basket_item_id = self.kwargs.get('pk')

        try:
            food_in_basket = OrderItem.objects.get(id=basket_item_id, order__customer=user)
        except OrderItem.DoesNotExist:
            raise NotFound('В корзине нет такого товара')

        if food_in_basket.order.customer != user:
            raise ValidationError('Это не ваша корзина')

        return food_in_basket

    def perform_destroy(self, instance):
        instance.delete()
        update_basket_total_price(get_or_create_pending_basket(self.request.user).first())


class ChangeProductQuantityAPIView(generics.UpdateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser]
    serializer_class = ChangeProductQuantitySerializer

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            return OrderItem.objects.filter(order__customer=user)

    def update(self, request, *args, **kwargs):
        food = self.get_object()
        serializer = self.get_serializer(food, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        update_basket_total_price(get_or_create_pending_basket(self.request.user).first())

        return Response(serializer.data)


class BasketProductsListAPIView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = BasketFoodsListSerializer
    parser_classes = [MultiPartParser]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user = self.request.user
            basket_id = self.kwargs.get('pk')

            return OrderItem.objects.filter(order=basket_id)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        basket_id = self.kwargs.get('pk')

        basket = Order.objects.filter(id=basket_id)
        if basket:
            return self.list(request, *args, **kwargs)

        return Response({'message': 'Карзина не существует'}, status=status.HTTP_404_NOT_FOUND)
