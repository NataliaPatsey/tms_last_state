from datetime import date,datetime
from django.db.models.functions import TruncYear, TruncMonth,TruncDay, TruncHour, TruncSecond, TruncMinute, TruncSecond

from django.db.models import Count, Avg
from re import findall
from .utils import get_plot,get_pie,get_bar

from django.http import HttpResponse
from django.urls import reverse

from .models import  Favore,PostRat,Categories,Tags, Post, LikeStatPost, PostComent, PreOrder, DAY
from django.shortcuts import render, get_object_or_404, redirect
from .forms import PostForm, SearchForms, CommemtForm, CategoryForms, RemarkForm
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
from django.db.models.functions import TruncMonth

# Create your views here.
# user registration
def categories_list(request):
    categories_lst = Categories.objects.all()
    return render(request, 'blog/categories_list.html', {'categories_lst': categories_lst})

def category_posts(request, cat_pk):
    form = CommemtForm()
    posts_lst = Post.objects.filter(cat_name__pk=cat_pk)
    return render(request, 'blog/category_post.html', {'posts_lst': posts_lst, 'form': form})


class RegisterFormView(FormView):
    form_class = UserCreationForm
    success_url = "/posts/"
    template_name = "blog/register.html"

    def form_valid(self, form):
        form.save()
        return super(RegisterFormView, self).form_valid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('posts_list')


class LoginFormView(FormView):
    form_class = AuthenticationForm
    template_name = "blog/login.html"
    success_url = "/posts/"

    def form_valid(self, form):
        self.user = form.get_user()

        login(self.request, self.user)
        return super(LoginFormView, self).form_valid(form)


def post_delete(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    post.delete()
    return redirect('posts_list')


def post_delete_confirm(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    return render(request, 'blog/post_delete.html', {'post': post})


def post_edit(request, post_pk):
    post = get_object_or_404(Post, pk=post_pk)
    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            if 'draft' in request.POST:
                if request.POST['draft'] == "1":
                    post.draft = 1
            else:
                post.draft = 0
            post.save()
            post.tags_set.clear()#clear retation
            pattern = r'#\w+'
            tag_lst = findall(pattern, post.text)
            for tg in tag_lst:
                if Tags.objects.filter(tag=tg).exists():
                    tag = Tags.objects.get(tag=tg)
                else:
                    tag = Tags(tag=tg)
                    tag.save()
                tag.post.add(post)
            #return render(request, 'blog/post_edit.html', {'form': form, 'draft': post.draft})
            return redirect('post_detail', post_pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'draft': post.draft})


def new_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():

            post = form.save(commit=False)
            if 'draft' in request.POST:
                if request.POST['draft'] == "1":
                    post.draft = 1
            else:
                 post.draft = 0
            post.author = request.user
            post.save()
            pattern = r'#\w+'
            tag_lst = findall(pattern,post.text)
            for tg in tag_lst:
                if Tags.objects.filter(tag=tg).exists():
                    tag = Tags.objects.get(tag=tg)
                else:
                    tag=Tags(tag=tg)
                    tag.save()

                tag.post.add(post)
            return redirect('post_detail', post_pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/new_post.html', {'form': form})


def posts_list(request):
    form = SearchForms()
    sauthor = ''
    posts = ''
    if request.method == 'POST':
        sauthor  = request.POST['search_by_author']
    if sauthor != '':
        posts = Post.objects.filter(author__username=sauthor, draft=0)
    else:
        posts = Post.objects.filter(draft=0)
    authors_list =  set(Post.objects.values_list('author__username', flat=True))
    return render(request, 'blog/posts_list.html', {'posts': posts, 'search_form':form, 'authors_list':authors_list })

def posts_draft(request):
    form = SearchForms()
    sauthor = ''
    posts = ''
    if request.method == 'POST':
        sauthor  = request.POST['search_by_author']
    if sauthor != '':
        posts = Post.objects.filter(author__username=sauthor, draft=1)
    else:
        posts = Post.objects.filter(draft=1)

    authors_list =  set(Post.objects.values_list('author__username', flat=True))

    return render(request, 'blog/posts_list.html', {'posts': posts, 'search_form':form, 'authors_list':authors_list})

def post_like(request, post_pk):
    sauthor = request.user
    post = Post.objects.get(pk=post_pk)
    if LikeStatPost.objects.filter(user=sauthor, post=post).count() !=0 :
        stat = LikeStatPost.objects.get(user=sauthor, post=post)
        stat.like_count = 1
        stat.dislike_count = 0
        stat.save()
    else:
        stat = LikeStatPost()
        stat.post = post
        stat.user = request.user
        stat.like_count = 1
        stat.dislike_count = 0
        stat.save()
    return redirect('post_detail', post_pk=post_pk)

def post_dislike(request, post_pk):
    sauthor = request.user
    post = Post.objects.get(pk=post_pk)
    if LikeStatPost.objects.filter(user=sauthor, post=post).count() != 0:
        stat = LikeStatPost.objects.get(user=sauthor, post=post)
        #stat = LikeStatPost.objects.filter(user=sauthor, article=post)
        stat.like_count = 0
        stat.dislike_count = 1
        stat.save()
    else:
        stat = LikeStatPost()
        stat.post = post
        stat.user = request.user
        stat.like_count = 0
        stat.dislike_count = 1
        stat.save()
    return redirect('post_detail', post_pk=post.pk)

def post_detail(request, post_pk, tag_lst=[]):
    #post = Post.objects.get(pk = post_pk)
    #post = Post.objects.filter(pk = post_pk)
    post = get_object_or_404(Post,pk=post_pk)
    post.views_count +=1
    post.save()
    cur_user = request.user
    posts_five = Post.objects.order_by('-create_date')[0:5]
    post_like = LikeStatPost.objects.filter(post__pk=post_pk , like_count = 1).count()
    post_dislike = LikeStatPost.objects.filter(post__pk=post_pk, dislike_count = 1).count()
    comments = PostComent.objects.filter(post__id=post_pk)
    new_comment = CommemtForm
    #--- post-of-today
    posts_of_day = Post.objects.filter(create_date__gte=date.today())
    count_com = len(comments)
    tags_lst = Tags.objects.filter(post=post)
    rat = post.mark_avg
    mark_count = post.mark_count
    favorite_stat = Favore.objects.filter(post__id=post_pk,user=request.user).exists()
    #annotate(post__pk=post_pk).Avg()

    return render(request, 'blog/post_detail.html', {'rat':rat,
                                                     'favorite_stat':favorite_stat,
                                                     'mark_count': mark_count,
                                                     'post': post,
                                                     'tags_lst' : tags_lst,
                                                     'cur_date': date.today(),
                                                     'posts_five':posts_five,
                                                     'posts_of_day': posts_of_day,
                                                     'cur_user':cur_user,
                                                     'post_like':post_like,
                                                     'post_dislike':post_dislike,
                                                     'comments':comments,
                                                     'new_comment':new_comment,
                                                     'count_com':count_com})

def new_comment(request, post_pk):
    if request.method == 'POST':
        form = CommemtForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.post = get_object_or_404(Post,pk=post_pk)
            comment.save()
            return redirect('post_detail', post_pk=post_pk)
    else:
        return redirect('post_detail', post_pk=post_pk)

def comment_edit(request, comm_pk):
    comm = get_object_or_404(PostComent, pk=comm_pk)
    form =''
    post = comm.post
    if request.method == 'POST':
        form = CommemtForm(request.POST, instance=comm)
        if form.is_valid():
            comm = form.save(commit=False)
            # post.author = request.user
            comm.save()
            return redirect('post_detail', post_pk=post.pk)
    else:
        form = CommemtForm(instance=comm)
    return render(request, 'blog/comm_edit.html',  {'form': form})

def stat(request):
    stat_user = LikeStatPost.objects.values('post','post__title').annotate(user_count=Count('user')).order_by('-user_count')
    stat_post = Post.objects.filter(draft=0).count()
    stat_draft = Post.objects.filter(draft=1).count()
    stat_user_post = Post.objects.values('author__username').annotate(user_post=Count('id'))
    stat_likes = LikeStatPost.objects.filter(like_count=1).values('post__id', 'post__title','like_count').annotate(likes_count=Count('like_count')).order_by('-likes_count')[0:5]
    stat_dislikes = LikeStatPost.objects.filter(dislike_count=1).values('post__id', 'post__title', 'dislike_count').annotate(dislikes_count=Count('dislike_count')).order_by('-dislikes_count')[0:5]

    # stat = PreOrder.objects.values('time').annotate(dcount=Count('time')).order_by('dcount')
    # for dct in stat:
    #     for tpl in DAY:
    #         if tpl[0] == dct['time']:
    #             dct['time_name'] = tpl[1]

    res_y = Post.objects.annotate(dt_part=TruncYear('create_date')).values('dt_part').annotate(dcount=Count('id'))
    x_y = [x['dt_part'].strftime('%Y') for x in res_y]
    y_y = [y['dcount'] for y in res_y]
    chart_y = get_pie(x_y,y_y,'YEARS')

    res_m = Post.objects.annotate(dt_part=TruncMonth('create_date')).values('dt_part').annotate(dcount=Count('id'))
    x_y = [x['dt_part'].strftime('%Y-%b')  for x in res_m]
    y_y = [y['dcount'] for y in res_m]
    chart_m = get_pie(x_y, y_y, 'MONTHS')

    res_d = Post.objects.annotate(dt_part=TruncDay('create_date')).values('dt_part').annotate(dcount=Count('id'))
    x_y = [x['dt_part'].strftime('%Y-%b-%d') for x in res_d]
    y_y = [y['dcount'] for y in res_d]
    chart_d = get_bar(x_y, y_y, 'DAYS')

    res_h = Post.objects.annotate(dt_part=TruncHour('create_date')).values('dt_part').annotate(dcount=Count('id'))
    x_y = [x['dt_part'].strftime('%Y-%b-%d (%H)')  for x in res_h]
    y_y = [y['dcount'] for y in res_h]
    chart_h = get_plot(x_y, y_y, 'HOURS')

    res_min = Post.objects.annotate(dt_part=TruncMinute('create_date')).values('dt_part').annotate(dcount=Count('id'))
    x_y = [x['dt_part'].strftime('%Y-%b-%d (%H-%M)') for x in res_min]
    y_y = [y['dcount'] for y in res_min]
    chart_min = get_plot(x_y, y_y, 'MINUTES',6)



    best_by_mark = PostRat.objects.values('post','post__title', 'post__id').annotate(davg=Avg('mark')).order_by('-davg')[0:5]

    return render(request, 'blog/statistic.html', {
                                                    'best_by_mark': best_by_mark,
                                                    'stat_dislikes': stat_dislikes,
                                                    'stat_likes': stat_likes,
                                                    'chart_min':chart_min,
                                                   'chart_h': chart_h,
                                                   'chart_d':chart_d,
                                                   'chart_m': chart_m,
                                                   'chart_y':chart_y,
                                                   'res_min':res_min,
                                                   'res_h':res_h,
                                                   'res_d':res_d,
                                                   'res_m':res_m,
                                                   'res_y':res_y,
                                                   'stat_user':stat_user,
                                                   'stat_post':stat_post,
                                                   'stat_draft':stat_draft,
                                                   'stat_user_post':stat_user_post})

def tags_list(request):
    old_tags_list = Tags.objects.all()
    for tag_obj in old_tags_list:
        if Post.objects.filter(tags__pk=tag_obj.pk).count() == 0:
            Tags.objects.filter(pk=tag_obj.pk).delete()
    tags_lst=Tags.objects.all()
    return render(request, 'blog/tags_list.html',{'tags_lst':tags_lst})

def posts_with_tag(request, tag_pk):
    posts_lst = Post.objects.filter(tags__pk=tag_pk)
    return render(request, 'blog/posts_with_tag.html',{'posts_lst':posts_lst})

def post_remark(request, post_pk):

    remark_lst = PostRat.objects.filter(post__pk=post_pk)
    post = Post.objects.get(pk = post_pk)
    if request.method == 'POST':
        form = RemarkForm(request.POST)
        if form.is_valid():
            remark = form.save(commit=False)
            remark.user = request.user
            remark.post = get_object_or_404(Post, pk=post_pk)
            remark.save()
    form = RemarkForm()
    return render(request, 'blog/post_remark.html',{'form': form, 'post': post, 'remark_lst': remark_lst})

def post_favorite(request):
    fav = Favore.objects.filter(user=request.user)
    return render(request, 'blog/post_favorite.html',{'fav': fav, 'user': request.user})

def add_favorite(request, post_pk):
        fav = Favore()
        fav.user=request.user
        post = Post.objects.get(pk=post_pk)
        fav.post = post
        fav.save()
        return redirect('post_detail', post_pk=post_pk)


def del_favorite(request, post_pk):
    user = request.user
    post = Post.objects.get(pk=post_pk)
    Favore.objects.filter(post=post, user=user).delete()
    Favore.objects.all()
    return redirect('post_detail', post_pk=post_pk)






