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
    goods_name = models.CharField(verbose_name='商品名称',max_length=30, primary_key=True)
    goods_number = models.IntegerField(verbose_name='数量')
    goods_price = models.FloatField(verbose_name='价格')

    class Meta:
        verbose_name_plural = '商品管理'
        verbose_name = '商品'

    def __str__(self):
        return self.goods_name

    def sales_volume(self):
        return self.goods_price*self.goods_number

    sales_volume.short_description = '总价格'
    goods_total = property(sales_volume)

class UserModel(models.Model):
    email = models.EmailField('邮箱')
    password = models.CharField('密码', max_length=256)
    name = models.CharField('姓名', max_length=20)
    age = models.IntegerField('年龄')
    birthday = models.DateField('生日')
    ip = models.GenericIPAddressField('IP')


