# Generated by Django 3.1.7 on 2021-03-09 18:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20210309_2150'),
    ]

    operations = [
        migrations.AlterField(
            model_name='postcoment',
            name='post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.post', verbose_name='Post'),
        ),
    ]
