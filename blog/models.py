from django.db import models
from django.db.models import Avg, Count

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Author')
    title = models.CharField(max_length=50, verbose_name='Title')
    text = models.TextField(verbose_name='Text')
    create_date= models.DateTimeField(auto_now_add=True, verbose_name='create_date')
    file = models.FileField(upload_to='img_blog',default='none')
    views_count = models.IntegerField(default=0, verbose_name='views_count')
    like_count = models.IntegerField(default=0, verbose_name='views_count')
    dislike_count = models.IntegerField(default=0, verbose_name='views_count')
    draft = models.IntegerField(default=0, verbose_name='draft')
    cat_name = models.ForeignKey('blog.Categories', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Category')

    def __str__(self):
        return f'{self.pk}=={self.title}'
    @property
    def count(self):
        return PostComent.objects.filter(post=self).count()

    @property
    def mark_avg(self):
        if PostRat.objects.filter(post=self).values('mark').annotate(davg=Avg('mark')):
            rat = PostRat.objects.filter(post=self).values('mark').annotate(davg=Avg('mark'))
            rat= rat [0]['davg']
        else:
            rat = 0
        return rat

    @property
    def mark_count(self):
        rat = PostRat.objects.filter(post=self).count()
        return rat

    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикация'


class Categories(models.Model):
    cat_name = models.CharField(max_length=50, verbose_name='Category')

    def __str__(self):
        return f'{self.cat_name}'

    class Meta:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категории'



class LikeStatPost(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Author')
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Author')
    like_count = models.IntegerField(default=0, verbose_name='like_count')
    dislike_count = models.IntegerField(default=0, verbose_name='dislike_count')

    def __str__(self):
        return f'{self.user}-{self.post}'

    class Meta:
        verbose_name = 'Счет'
        verbose_name_plural = 'Счет'

class PostComent(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Author')
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Post')
    text = models.TextField(verbose_name='Text')
    create_date= models.DateTimeField(auto_now_add=True, verbose_name='Data')

    def __str__(self):
        return f'{self.user}--{self.post}'

    class Meta:
        verbose_name = 'Комент'
        verbose_name_plural = 'комент'

class PostRat(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Author')
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Post')
    mark = models.IntegerField (default=3 ,verbose_name='Mark')
    remark = models.CharField(max_length=50, blank=True, null=True, verbose_name='remark')

    def __str__(self):
        return f'{self.user}--{self.post}--{self.remark}'

    class Meta:
        verbose_name = 'Рейтинг'
        verbose_name_plural = 'Рейтинг'





class Tags(models.Model):
    tag = models.TextField(verbose_name='Tag')
    post = models.ManyToManyField(Post,verbose_name='ToPost')

    def __str__(self):
        return f'{self.pk}--{self.tag}--{self.post}'
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Тег'





# Create your models here.
DAY = ((1, 'morning'),
       (2, 'day'),
       (3, 'evaning'),)

class PreOrder(models.Model):
    name = models.CharField(max_length=50, verbose_name='name')
    time = models.IntegerField(verbose_name='patr_of_day', choices=DAY)
    phone = models.IntegerField(verbose_name='phone')
    date_in= models.DateField(auto_now_add=True, verbose_name='date_in')

    def __str__(self):
        return f'{self.name}--{self.phone}--{self.time}'

    class Meta:
        verbose_name = 'PreOrder'
        verbose_name_plural = 'PreOrder'

class Favore(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Author')
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, blank=True, null=True, verbose_name='Post')

    def __str__(self):
        return f'{self.user}--{self.post}'

    class Meta:
        verbose_name = 'Favore'
        verbose_name_plural = 'Favore'