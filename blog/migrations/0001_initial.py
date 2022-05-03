# Generated by Django 3.1.7 on 2021-02-25 18:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='заголовок')),
                ('text', models.TextField()),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
