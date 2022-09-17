from django.db import models

# Create your models here.


class Item(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    price = models.FloatField(default=0)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    data_json = models.JSONField(default={'item_ids': [], 'discounts': [], 'taxes': []})
    total_scale = models.FloatField(default=0)


class Tax(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    percentage = models.FloatField(default=0)
    inclusive = models.BooleanField(default=False)


class Discount(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    type = models.CharField(max_length=50, default='coupon')

