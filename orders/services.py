from orders.models import OrderModel
from orders.models import OrderProductsModel


class CartError(Exception):
    pass


def make_order(cart):
    from cart.models import CartItemModel
    if cart.status != 'not available':
        order = OrderModel.objects.create(
            user=cart.user,
            total_price=sum(
                [i.quantity*i.product.price for i in CartItemModel.objects.filter(cart=cart.id)])
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
