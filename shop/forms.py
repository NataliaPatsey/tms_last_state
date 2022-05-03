from shop.models import Goods, Card, Profile
from django import forms

class Form_Goods(forms.ModelForm):
    class Meta():
        model = Goods
        fields =('name', 'about','price', 'category', 'file')

class Form_card(forms.ModelForm):
    class Meta():
        model = Card
        fields =('card_name', 'card_number','card_month', 'card_year')

class Form_profile(forms.ModelForm):
    class Meta():
        model = Profile
        fields = ('first_name','last_name','email', 'br_date','file')