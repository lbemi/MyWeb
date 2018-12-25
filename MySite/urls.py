from django.urls import path, include
from MySite import views
from django.views.static import serve


urlpatterns = [
    path('',views.index ),
    path('trans/', views.trans),
    path('trans2/<str:from_lang>/<str:to_lang>/<str:words>',views.trans2),
    path('news_list/<str:news_type>',views.news_list),
    path('fiter/', views.fiter_test),
    path('all/',views.searchall),
    path('search_name/',views.search_name),
    path('search_price/', views.search_price),
    path('search_sort/', views.search_sort),
    path('register/',views.register),
    path('check/', views.check_user),
    path('reg/',views.reg),
    path('goods_list/', views.goods_list),
    path('add/', views.add_goods),
    path('del/',views.del_goods),
    path('search/',views.search),
    path('user_name/', views.get_name),
    path('send_email/', views.send_email),
    path('email/', views.wirte_email),
    path('re/', views.re),
    path('exit/', views.exit),
]
