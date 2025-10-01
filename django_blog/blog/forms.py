from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from taggit.forms import TagWidget
from taggit.models import Tag
from .models import Post
from .models import Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3})
        }
class PostForm(forms.ModelForm):
    tags = forms.CharField(
        required=False,
        help_text='Comma-separate tags (e.g. django, python)'
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'tags' : TagWidget(),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        raw = self.cleaned_data.get('tags', '')
        names = [n.strip() for n in raw.split(',') if n.strip()]
        if commit:
            instance.save()
            instance.tags.clear()
            for name in names:
                tag, _ = Tag.objects.get_or_create(name=name)
                instance.tags.add(tag)
        return instance
class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email']
