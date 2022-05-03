from django.contrib import admin
from  blog.models import Favore,PostRat,Categories, Post, PostComent, LikeStatPost, PreOrder, Tags

# Register your models here.
admin.site.register(Post)
admin.site.register(PostComent)
admin.site.register(LikeStatPost)
admin.site.register(PreOrder)
admin.site.register(Tags)
admin.site.register(Categories)
admin.site.register(PostRat)
admin.site.register(Favore)