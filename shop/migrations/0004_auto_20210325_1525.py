# Generated by Django 3.1.7 on 2021-03-25 12:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0003_basket_goods_in_basket'),
    ]

    operations = [
        migrations.AddField(
            model_name='goods',
            name='file',
            field=models.FileField(default='none', upload_to='img_shop'),
        ),
        migrations.AlterField(
            model_name='goods_in_basket',
            name='good',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.goods', verbose_name='Good'),
        ),
    ]
