from django.db import models


class Cryptocurrency(models.Model):
    name    = models.CharField(max_length=50)
    symbol  = models.CharField(max_length=15, unique=True)
    rank    = models.IntegerField()

    def __str__(self):
        return self.symbol

class OrderHistory(models.Model):
    user = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    symbol = models.CharField(max_length=15)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    quantity = models.DecimalField(max_digits=20, decimal_places=10)
    type = models.CharField(max_length=5)

class AssetHistory(models.Model):
    user = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)
    value = models.DecimalField(max_digits=20, decimal_places=2)

