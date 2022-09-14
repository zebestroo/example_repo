from django.db import models

# Create your models here.


class Item(models.Model):
    id = models.CharField(primary_key=True, max_length=50)
    name = models.CharField(max_length=50)
    description = models.TextField(max_length=500)
    price = models.FloatField(default=0)
