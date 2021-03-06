# Generated by Django 3.1.7 on 2021-04-04 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0013_auto_20210404_0003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.FileField(default='none', upload_to='users_photo', verbose_name='avatar'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='br_date',
            field=models.DateField(verbose_name='br_date'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='email',
            field=models.EmailField(default='None', max_length=64, verbose_name='email'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='first_name',
            field=models.CharField(default='None', max_length=64, verbose_name='first_name'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='last_name',
            field=models.CharField(default='None', max_length=64, verbose_name='last_name'),
        ),
    ]
