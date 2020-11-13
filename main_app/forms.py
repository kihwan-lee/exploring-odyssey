from django.forms import ModelForm
from .models import Author, Article, Comment, Location

class Profile_Form(ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'location', 'imageURL'] # 'location'

class Article_Form(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        # removed 'city' from form

class Comment_Form(ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class Search_Form(ModelForm):
    class Meta:
        model = Location
        fields = ('location',)