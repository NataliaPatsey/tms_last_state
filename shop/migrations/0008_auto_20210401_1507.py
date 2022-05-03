# Generated by Django 3.1.7 on 2021-04-01 12:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0007_auto_20210401_1453'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_month',
            field=models.CharField(max_length=2, verbose_name='Month'),
        ),
        migrations.AlterField(
            model_name='card',
            name='card_name',
            field=models.CharField(default='My card', max_length=16, verbose_name='Card_Name'),
        ),
        migrations.AlterField(
            model_name='card',
            name='card_year',
            field=models.CharField(max_length=2, verbose_name='Year'),
        ),
    ]