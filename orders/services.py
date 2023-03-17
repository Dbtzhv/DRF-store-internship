from orders.models import OrderProductsModel, OrderModel


def place_order(self):
    order = OrderModel.objects.create(
        user=self.user,
    )

    for item in self.items.all():
        OrderProductsModel.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
        )

    for item in self.items.all():
        item.product.quantity -= item.quantity
        item.product.save()
        if item.product.quantity <= 0:
            item.delete()

    self.status = 'p'
    self.save()
