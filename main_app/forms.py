from django.forms import ModelForm
from .models import Author, Article

class Profile_Form(ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'city', 'imageURL']

class Article_Form(ModelForm):
    class Meta:
        model = Article
        fields = ['title', 'content']
        # removed 'city' from form

