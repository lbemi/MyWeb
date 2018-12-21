from django.db import models

class Goods(models.Model):
    goods_name = models.CharField(max_length=30)
    goods_number = models.IntegerField()
    goods_price = models.FloatField()

    def __str__(self):
        return self.goods_name


class Users(models.Model):
    user_name = models.CharField(max_length=20, primary_key=True)
    password = models.CharField(max_length=16)



class GoodsInfo(models.Model):
    goods_name = models.CharField(max_length=30, primary_key=True)
    goods_number = models.IntegerField()
    goods_price = models.FloatField()