from django.db import models
from django.conf import settings
from Shop_app.models import Product
# Create your models here.


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='cart')
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quatity = models.IntegerField(default=1)
    purchased = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    def __str__(self) -> str:
        return f'{self.quatity} x {self.item.name}'


    def get_total(self):
        total = self.item.price * self.quatity
        float_total = format(total, '0.2f')
        return float_total

class Order(models.Model):
    order_items = models.ManyToManyField(Cart)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    paymentID = models.CharField(max_length=264, blank=True, null=True)
    orderID = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self) -> str:
        return self.user.profile.username +"'s"+' order'

    def get_totals(self):
        total = 0
        for order_item in self.order_items.all():
            total += float(order_item.get_total())
        return total