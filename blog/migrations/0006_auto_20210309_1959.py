# Generated by Django 3.1.7 on 2021-03-09 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_post_views_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='dislike_count',
            field=models.IntegerField(default=0, verbose_name='views_count'),
        ),
        migrations.AddField(
            model_name='post',
            name='like_count',
            field=models.IntegerField(default=0, verbose_name='views_count'),
        ),
        migrations.AlterField(
            model_name='post',
            name='views_count',
            field=models.IntegerField(default=0, verbose_name='views_count'),
        ),
    ]