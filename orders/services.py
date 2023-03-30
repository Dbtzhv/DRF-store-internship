from orders.models import OrderModel
from orders.models import OrderProductsModel
from utils.exceptions import CartError
from django.db.models import Sum, F


def make_order(cart):
    from cart.models import CartItemModel

    total_price = float(CartItemModel.objects.filter(cart=cart).aggregate(
        total_price=Sum(F('quantity') * F('product__price')))['total_price'] or 0)

    if cart.status != 'not available':
        order = OrderModel.objects.create(
            user=cart.user,
            total_price=total_price
        )

        for item in CartItemModel.objects.filter(cart=cart.id):
            OrderProductsModel.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                product_price=item.product.price
            )

            item.product.general_quantity -= item.quantity
            item.product.save()

        cart.status = 'ordered'
        cart.save()

    else:
        raise CartError("Корзина содержит товары со статусом 'недоступен'")
