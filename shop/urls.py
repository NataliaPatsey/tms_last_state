from django.contrib import admin
from django.urls import path, include
from shop.views import qs_test, user_page,popular,order_list,order,add_to_basket ,user_profile,card_detail,add_card,goods_new ,goods_list, find_by_category, basket, delfrombasket,clearbasket


urlpatterns = [
    path('', goods_list, name='goods_list'),
    path('findbycategory/<int:category_pk>', find_by_category, name='find_by_category'),
    path('newgoods/', goods_new, name='new_goods'),
    path('basket/<int:messg_code>', basket, name='basket'),
    path('delfrombasket/<int:pk_good_in_basket>', delfrombasket, name='delfrombasket'),
    path('clearbasket/', clearbasket, name='clearbasket'),
    path('addcard/', add_card, name='add_card'),
    path('userpage/', user_page, name='user_page'),
    path('carddetail/<int:card_pk>', card_detail, name='card_detail'),
    path('addtobasket/<int:good_pk>', add_to_basket, name='add_to_basket'),
    path('order/', order, name='order'),
    path('orderlist/', order_list, name='order_list'),
    path('popular/', popular, name='popular'),
    path('userprofile/', user_profile, name='user_profile'),
    path('qstest/', qs_test, name='qs_test'),

]

