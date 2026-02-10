from tkinter.constants import CASCADE

from django.db import models
from django.contrib.auth.models import User, AbstractUser, Group


class Pvz(models.Model):
    index = models.DecimalField(max_digits=10, decimal_places=2)
    city = models.CharField(max_length=255)
    street = models.CharField(max_length=255)
    number = models.DecimalField(max_digits=10, decimal_places=2)

class Producer(models.Model):
    name = models.CharField(max_length=255)

class Manufacturer(models.Model):
    name = models.CharField(max_length=255)

class CategoryProduct(models.Model):
    name = models.CharField(max_length=255)

class StatusOrder(models.Model):
    name = models.CharField(max_length=255)

class Product(models.Model):
    article = models.CharField(max_length=255)
    product = models.CharField(max_length=255)
    unit = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    producer = models.ForeignKey(Producer, on_delete=models.CASCADE)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE)
    category = models.ForeignKey(CategoryProduct, on_delete=models.CASCADE)
    discount = models.DecimalField(max_digits=10,decimal_places=2)
    amount_on_warehouse = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=255)
    image = models.ImageField()

    def get_final_price(self):
        if self.discount > 0:
            return self.price * (100 - self.discount) / 100
        return self.price

class Order(models.Model):
    number_order = models.DecimalField(max_digits=10, decimal_places=2)
    arcticle = models.CharField(max_length=255)
    amount_product = models.DecimalField(max_digits=10, decimal_places=2)
    date_order = models.DateField()
    date_delivery = models.DateField()
    pvz = models.ForeignKey(Pvz, on_delete=models.CASCADE)
    client = models.ForeignKey(User, on_delete=models.CASCADE)
    code = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.ForeignKey(StatusOrder, on_delete=models.CASCADE)