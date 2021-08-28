from django.db import models
from django.core.validators import MaxValueValidator

from orders_app.enums import OrderStatus


class Order(models.Model):
    status = models.IntegerField(choices=OrderStatus.choices, default=OrderStatus.OPENED.value)
    created_at = models.DateTimeField(auto_now_add=True)
    product = models.ForeignKey('orders_app.Product', related_name='orders', on_delete=models.RESTRICT)


class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    discount = models.DecimalField(
        max_digits=5, decimal_places=2, validators=[MaxValueValidator(100.00)], default=0
    )


class Bill(models.Model):
    order = models.ForeignKey('orders_app.Order', related_name='bills', on_delete=models.RESTRICT)
    created_at = models.DateTimeField(auto_now_add=True)
