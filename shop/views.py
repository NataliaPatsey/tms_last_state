from functools import reduce

from django.db.models import Sum, Count
from django.shortcuts import render,redirect, get_object_or_404
from shop.models import Profile,Goods_in_order, Goods, Categories, Basket, Goods_in_basket, Card, Order
from shop.forms import Form_Goods, Form_card, Form_profile
from django.conf import settings
from django.core.mail import send_mail
import requests

# Create your views here.

def goods_list(request):
    goods_lst  = Goods.objects.all()
    categories_lst = Categories.objects.all()
    amount_goods = Goods_in_basket.objects.filter(basket__user=request.user).aggregate(Sum('count'))
    return render(request, 'shop/goods_list.html', {'goods_lst':goods_lst, 'categories_lst': categories_lst, 'amount_goods':amount_goods})

def find_by_category(request, category_pk):
    goods_lst  = Goods.objects.filter(category__pk=category_pk)
    categories_lst = Categories.objects.all()
    return render(request, 'shop/goods_list.html', {'goods_lst':goods_lst , 'categories_lst': categories_lst})

def goods_new(request):
    messg=''
    if request.method == 'POST':
        form = Form_Goods(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messg = 'It\'s ok'
        else:
            messg = 'Something wrongs ('
    form = Form_Goods()
    return render(request, 'shop/goods_new.html', {'form': form, 'messg':messg})

def basket(request, messg_code):
    my_lst = Goods_in_basket.objects.filter(basket__user=request.user)
    amount_money = 0
    for good in my_lst:
        amount_money += good.full_price
    messg = ''
    if messg_code == 0:
        messg = ''
    elif messg_code == 1:
        messg = 'Email is sent. Your order is in process'
    elif messg_code == 2:
        messg = 'Email is NOT send. Your is not finished'
    elif messg_code == 3:
        messg = 'All is removed'
    elif messg_code == 4:
        messg = 'OOOUPs, likes you are a robot'
    elif messg_code == 5:
        messg = 'OOOUPs, likes your basket is empty'

    return render(request, 'shop/basket.html', {'my_lst': my_lst, 'amount_money':amount_money, 'messg':messg })

def delfrombasket(request, pk_good_in_basket):
    good = get_object_or_404(Goods_in_basket, pk=pk_good_in_basket)
    good.delete()
    return redirect('basket', messg_code = 3)

def clearbasket(request):
    Goods_in_basket.objects.filter(basket__user=request.user).delete()
    return redirect('basket', messg_code=3)

def add_card(request):
    messg =''
    if request.method == 'POST':
        card_form = Form_card(request.POST)
        if card_form.is_valid():
            card = card_form.save(commit=False)
            card.user = request.user
            if card.card_year.isdigit() and card.card_month.isdigit():
                if len(str(card.card_number)) == 16 and ( 0 < int(card.card_month) < 13) and ( 20 <= int(card.card_year) <= 99):
                    card.save()
                    messg = 'It\'s ok'
                else:
                    messg = 'Length of values is wrong ('
            else:
                messg = 'Type of values is wrong ('
    form = Form_card()
    return render(request,'shop/add_card.html', {'form': form, 'messg': messg })

def user_page(request):
    card_lst = Card.objects.filter(user=request.user)
    for card in card_lst:
        card.card_number = 'XXXX-XXXX-XXXX-'+str(card.card_number)[12:]
    goods_count = Goods_in_basket.objects.filter(basket__user=request.user).count()
    my_lst = Goods_in_basket.objects.filter(basket__user=request.user)
    amount_money = 0
    for good in my_lst:
        amount_money += good.full_price
    profile = ''
    if Profile.objects.filter(user=request.user).exists():
        profile = Profile.objects.get(user=request.user)
    else:
        profile = Profile()
    return render(request, 'shop/user_page.html', {'card_lst': card_lst, 'goods_count':goods_count, 'amount_money':amount_money , 'profile':profile })

def card_detail(request, card_pk):
    card = get_object_or_404(Card, pk=card_pk)
    card.card_number = 'XXXX-XXXX-XXXX-' + str(card.card_number)[12:]
    return render(request, 'shop/card_detail.html', {'card': card })

def add_to_basket(request, good_pk):
    if Goods_in_basket.objects.filter(good__pk=good_pk, basket__user=request.user).count() == 0:
        good = Goods_in_basket()
        good.basket = Basket.objects.get(user=request.user)
        good.good = Goods.objects.get(pk=good_pk)
        good.count = 1
        good.save()
    else:
        good = Goods_in_basket.objects.get(good__pk=good_pk, basket__user=request.user)
        good.count += 1
        good.save()
    return redirect('goods_list')


def order(request):
    messg_code = 0
    ''' Begin reCAPTCHA validation '''
    recaptcha_response = request.POST.get('g-recaptcha-response')
    data = {
        'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
        'response': recaptcha_response
    }
    r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
    result = r.json()
    ''' End reCAPTCHA validation '''
    if result['success']:
        if Goods_in_basket.objects.filter(basket__user=request.user).exists():
            if Profile.objects.filter(user=request.user).values('email').exists():
                order = Order.objects.create(user=request.user)
                order.save()
                data = 'Your order in process\n'
                goods_lst = Goods_in_basket.objects.filter(basket__user=request.user)
                for item in goods_lst:
                    Goods_in_order.objects.create(order=order, good=item.good, count=item.count)
                    data += f'{item.good.name} / {item.count} \n'
                Goods_in_basket.objects.filter(basket__user=request.user).delete()
                #messg_code = 0
                profile = Profile.objects.get(user=request.user)
                send_mail('Welcome to APPShop!', data, settings.EMAIL_HOST_USER,
                          [profile.email], fail_silently=False)
                messg_code = 1
            else:
                messg_code = 2
        else:
            messg_code = 5
    else:
        messg_code = 4
    return redirect('basket', messg_code=messg_code)

def order_list(request):
    order_lst = Goods_in_order.objects.filter(order__user= request.user)
    return render(request, 'shop/order_list.html', {'order_lst': order_lst })

def popular(request):
    popular_test = Goods_in_order.objects.values('good__name').annotate(count=Count('pk')).order_by('-count')

    popular = dict()
    for item in Goods_in_order.objects.all():
        popular[item.good.name] = popular.get(item.good.name, 0) + 1
    tmp = sorted(popular, key=popular.get, reverse=True)
    popular_result = dict()
    for product in tmp:
        popular_result[product] = popular[product]
    return render(request, 'shop/popular.html', {'popular': popular_result , 'popular_test':popular_test[0:3]})

def user_profile(request):
    messg = ''
    if not Profile.objects.filter(user=request.user).exists() and request.method != 'POST':
        messg = 'empry'
        form = Form_profile()
        profile = Profile()
    elif Profile.objects.filter(user=request.user).exists() and request.method != 'POST':
        profile = get_object_or_404(Profile, user=request.user)
        form = Form_profile(instance=profile)
    elif request.method == 'POST':
        if Profile.objects.filter(user=request.user).exists():
            profile = get_object_or_404(Profile, user=request.user)
        else:
            profile = Profile()
        form = Form_profile(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            ''' Begin reCAPTCHA validation '''
            recaptcha_response = request.POST.get('g-recaptcha-response')
            data = {
                'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
                'response': recaptcha_response
            }
            r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=data)
            result = r.json()
            ''' End reCAPTCHA validation '''
            if result['success']:
                profile = form.save(commit=False)
                profile.user = request.user
                profile.save()
                #profile = get_object_or_404(Profile, user=request.user)
                form = Form_profile(request.POST, request.FILES, instance=profile)
                messg = 'It\'s ok'
            else:
                messg = 'likes you are a robot'
        else:
            messg = 'Something wrongs ('
    return render(request, 'shop/user_profile.html', {'form': form, 'messg': messg,'profile': profile})


def qs_test(request):
    data=Card.objects.filter(id__lt=3)
    return render(request, 'shop/qs_test.html',{'data': data})



