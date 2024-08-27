from django.db import models

# Create your models here.
class Cart(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    product = models.ForeignKey('menu.Item', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'carts'
        verbose_name = 'cart'
        verbose_name_plural = 'carts'

    def __str__(self):
        return f'{self.user} - {self.product} - {self.quantity}'

    def get_total(self):
        return self.product.price * self.quantity

class Order(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        verbose_name = 'order'
        verbose_name_plural = 'orders'

    def __str__(self):
        return f'{self.user} - {self.total}'


class OrderItems(models.Model):
    order = models.ForeignKey('cart.Order', on_delete=models.CASCADE)
    product = models.ForeignKey('menu.Item', on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_items'
        verbose_name = 'order item'
        verbose_name_plural = 'order items'

    def __str__(self):
        return f'{self.order} - {self.product} - {self.quantity}'

    def get_total(self):
        return self.product.price * self.quantity