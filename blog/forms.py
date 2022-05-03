from .models import Post, PostComent, Categories,PostRat
from django import forms

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'file', 'cat_name')

class SearchForms(forms.Form):
    lst = Post.objects.values_list('author__username', flat=True)
    lst = set(lst)
    search_by_author = forms.ChoiceField(choices=zip(lst,lst))

class CategoryForms(forms.Form):
    lst = Categories.objects.all()
    search_by_cat = forms.ChoiceField(choices=zip(lst,lst))


class CommemtForm(forms.ModelForm):
    class Meta:
        model = PostComent
        fields = ('text',)

class RemarkForm(forms.ModelForm):
    class Meta:
        model = PostRat
        fields = ('mark', 'remark')