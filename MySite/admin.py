from django.contrib import admin
from MySite.models import GoodsInfo,UserModel, SunmerNoteTest
from django_summernote.admin import SummernoteModelAdmin

class goodsinfo(admin.ModelAdmin):
    list_display = ('goods_name','goods_number','goods_price','goods_total')

class SummerNoteTestAdmin(SummernoteModelAdmin):
    summernote_fields = '__all__'

admin.site.register(GoodsInfo, goodsinfo)
admin.site.register(UserModel)
admin.site.register(SunmerNoteTest, SummerNoteTestAdmin)

