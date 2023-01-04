from django import forms


from .models import Comment, Tag, Post
from django.contrib.auth.models import User


class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=25)
    email = forms.EmailField()
    to = forms.EmailField()
    comments = forms.CharField(
        required=False,
        widget=forms.Textarea)


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


class TagForm(forms.ModelForm):

    class Meta:
        model = Tag
        fields = ('tag_name',)


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        # fields = ('title', 'slug', 'author', 'body', 'publish', 'status', 'tags',)
        fields = '__all__'
        exclude = ('slug', 'author',)
        widgets = {'body': forms.Textarea(attrs={'style': 'height: 20em; width: 65em'}), }


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = User
        fields = '__all__'
        exclude = ('last_login', 'is_superuser', 'is_staff', 'date_joined', 'user_permissions', 'groups', 'password')
        # default = {'author_id': 'user.get_id'}
