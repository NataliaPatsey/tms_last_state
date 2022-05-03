from django.contrib import admin
from django.urls import path, include
from blog.views import del_favorite,add_favorite, post_favorite,post_remark ,category_posts,categories_list,posts_with_tag, tags_list, posts_draft,stat, comment_edit, new_comment, LogoutView, LoginFormView, RegisterFormView, posts_list, post_detail, new_post, post_edit, post_delete_confirm,post_delete, post_like, post_dislike

urlpatterns = [
    path('', posts_list, name='posts_list'),
    path('detail/<int:post_pk>', post_detail, name='post_detail'),
    path('new/', new_post, name='new_post'),
    path('edit/<int:post_pk>', post_edit, name='post_edit'),
    path('delete_confirm/<int:post_pk>', post_delete_confirm, name='post_delete_confirm'),
    path('delete/<int:post_pk>', post_delete, name='post_delete'),
    path('register/', RegisterFormView.as_view(), name='register'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('like/<int:post_pk>', post_like, name='post_like'),
    path('dislike/<int:post_pk>', post_dislike, name='post_dislike'),
    path('new_comment/<int:post_pk>', new_comment, name='new_comment'),
    path('comment_edit/<int:comm_pk>', comment_edit, name='comment_edit'),
    path('stat/', stat, name='stat'),
    path('posts_draft', posts_draft, name='posts_draft'),
    path('tags', tags_list, name='tags_list'),
    path('postswithtag/<int:tag_pk>', posts_with_tag, name='posts_with_tag'),
    path('categories', categories_list, name='categories_list'),
    path('categorypost/<int:cat_pk>', category_posts, name='category_posts'),
    path('post_remark/<int:post_pk>', post_remark, name='post_remark'),
    path('postfavorite/', post_favorite, name='post_favorite'),
    path('addfavorite/<int:post_pk>', add_favorite, name='add_favorite'),
    path('delfavorite/<int:post_pk>', del_favorite, name='del_favorite'),
]
