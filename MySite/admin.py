from django.contrib import admin
from MySite.models import GoodsInfo


class goodsinfo(admin.ModelAdmin):
    list_display = ('goods_name','goods_number','goods_price','goods_total')

admin.site.register(GoodsInfo, goodsinfo)

