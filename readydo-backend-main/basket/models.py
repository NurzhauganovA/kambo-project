from django.db import models

from auth_user.models import User
from common.models import BaseModel
from foods.models import Food


class OrderChoices(models.IntegerChoices):
    PENDING = 1, 'pending'
    SHOPPED = 2, 'shopped'
    DELIVERED = 3, 'delivered'

    @staticmethod
    def get_status(status):
        if status == OrderChoices.PENDING:
            return 'pending'
        elif status == OrderChoices.SHOPPED:
            return 'shipped'
        elif status == OrderChoices.DELIVERED:
            return 'delivered'
        return ''


class Order(BaseModel):
    customer = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    date_ordered = models.DateTimeField(auto_now_add=True)
    status = models.PositiveSmallIntegerField(choices=OrderChoices.choices, default=OrderChoices.PENDING)
    total_price = models.DecimalField(max_digits=10, decimal_places=0, default=0)

    def __str__(self):
        return f"Order {self.id}"


class OrderItem(BaseModel):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.food.name}"
