# Generated by Django 3.1.7 on 2021-03-11 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_auto_20210311_1555'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='draft',
            field=models.IntegerField(default=0, verbose_name='draft'),
        ),
    ]