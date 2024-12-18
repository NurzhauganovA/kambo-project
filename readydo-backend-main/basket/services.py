from auth_user.models import User
from basket.models import Order, OrderChoices, OrderItem


def get_or_create_pending_basket(user: User) -> Order:
    last_basket_status = Order.objects.filter(customer=user).order_by('-created_at')

    if last_basket_status and last_basket_status.first().status == OrderChoices.PENDING:
        return last_basket_status
    else:
        Order.objects.create(customer=user, status=OrderChoices.PENDING)
        return Order.objects.filter(customer=user).order_by('-created_at')


def update_basket_total_price(basket):
    total_price = 0
    basket_foods = OrderItem.objects.filter(order=basket)
    for food in basket_foods:
        total_price += food.quantity * food.food.price
    basket.total_price = total_price
    basket.save(update_fields=['total_price'])
