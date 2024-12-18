from django.contrib import admin

from basket.models import Order, OrderItem


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'customer', 'date_ordered', 'status', 'total_price']
    search_fields = ['id', 'customer', 'status']
    ordering = ['id', 'status']


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['id', 'food', 'quantity', 'order']
    search_fields = ['food', 'quantity']
    ordering = ['id']
