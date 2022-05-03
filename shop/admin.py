from django.contrib import admin
from shop.models import Profile,Goods_in_order,Order,Goods, Categories, Basket, Goods_in_basket, Card
# Register your models here.
admin.site.register(Goods)
admin.site.register(Categories)
admin.site.register(Basket)
admin.site.register(Goods_in_basket)
admin.site.register(Card)
admin.site.register(Order)
admin.site.register(Goods_in_order)
admin.site.register(Profile)
