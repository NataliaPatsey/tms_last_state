from django.db import models
from decimal import  Decimal
# Create your models here.

class Goods(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name_of_good')
    about = models.CharField(max_length=50, verbose_name='About_good')
    price = models.DecimalField(max_digits=6, decimal_places=2, default=Decimal("0.00"))
    category = models.ForeignKey('shop.Categories',  on_delete=models.CASCADE,blank=True, null=True, verbose_name='Category')
    file = models.FileField(upload_to='img_shop', default='none')

    def __str__(self):
        return self.name

class Categories(models.Model):
    name = models.CharField(max_length=50, verbose_name='Category')

    def __str__(self):
        return self.name

class Basket(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE, verbose_name='User')

    def __str__(self):
        return self.user.username


class Goods_in_basket(models.Model):
    basket = models.ForeignKey('shop.Basket', on_delete=models.CASCADE, verbose_name='Basket')
    good = models.ForeignKey('shop.Goods', on_delete=models.CASCADE, verbose_name='Good')
    count = models.PositiveIntegerField(default=1, verbose_name='Count')

    def __str__(self):
        return f'{self.basket}--{self.good}--{self.count}'

    @property
    def full_price(self):
        prise_float=float(self.good.price)
        return self.count * prise_float

class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE,  verbose_name='User')
    status = models.CharField(max_length=32, verbose_name='Status', default='in process')

    def __str__(self):
        return self.status

class Goods_in_order(models.Model):
    good = models.ForeignKey('shop.Goods', on_delete=models.CASCADE, verbose_name='Good')
    order = models.ForeignKey('shop.Order',on_delete=models.CASCADE, verbose_name='User')
    count = models.PositiveIntegerField(default=1, verbose_name='Count')

    def __str__(self):
        return f'{self.order}--{self.count}'


class Card(models.Model):
    card_name = models.CharField(max_length=16, default='My card', verbose_name='Card_Name')
    card_number = models.IntegerField(verbose_name='Card_num',default=False,blank=False)
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='User')
    card_year = models.CharField(max_length=2 ,verbose_name='Year',blank=False)
    card_month = models.CharField(max_length=2, verbose_name='Month',blank=False)

    def __str__(self):
        return f'{self.card_number}'

class Profile(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name='User')
    first_name = models.CharField(max_length=64, default='None', verbose_name='first_name')
    last_name = models.CharField(max_length=64, default='None',verbose_name='last_name')
    br_date = models.DateField(verbose_name='br_date')
    email = models.EmailField(max_length=64,default='None', verbose_name='email')
    file = models.FileField(upload_to='users_photo', default='none', verbose_name='file')

