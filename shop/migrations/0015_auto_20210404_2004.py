# Generated by Django 3.1.7 on 2021-04-04 17:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0014_auto_20210404_1829'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='avatar',
        ),
        migrations.AddField(
            model_name='profile',
            name='file',
            field=models.FileField(default='none', upload_to='users_photo', verbose_name='file'),
        ),
    ]
