from MySite.models import Goods
import os
import django

#
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MyWeb.settings")  # 关联默认设置
# django.setup()  # 装载Django

with open('data','r',encoding='utf-8') as file:
    for line in file:
        lst = line.strip().split(',')
        print(lst)
        state = Goods.objects.create(goods_name = lst[0],
                                     goods_number = lst[1],
                                     goods_price = lst[2])
        print(state)