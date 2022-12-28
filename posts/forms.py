from django import forms

from .models import Post, Coment

class PostForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ['title', 'body']

    
class ComentForm(forms.ModelForm):
    class Meta():
        model = Post
        fields = ['body']