# Generated by Django 3.1.7 on 2021-03-18 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0017_postrat'),
    ]

    operations = [
        migrations.AddField(
            model_name='postrat',
            name='title',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='remark'),
        ),
    ]
