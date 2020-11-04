from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import City, Author, Article
from main_app.forms import Article_Form
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
#from .forms import

#-------------------------------------- ADMIN/AUTH
def signup(request):
    error_message=''

    if request.method == 'POST':
        user_form = UserCreationForm(data = {'username':request.POST['username'], 'password1': request.POST['password1'], 'password2': request.POST['password2']})
        # article_form = Article_Form(data = {'name': request.POST['name'], 'city': request.POST['city']})
        if user_form.is_valid():
            user = user_form.save()
            #new_form.user_id = user.id 

            login(request, user)
            return redirect('home') #needs to change to profile when made
        else:
            error_message='Invalid sign-up try again'
    else:
        user_form=UserCreationForm()

    context = {'user_form': user_form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)


# ------------------------------------- STATIC PAGES
def home (request):
    login_form = AuthenticationForm()
    return render(request, 'home.html', {'form': login_form})

def about(request):
    return render(request, 'about.html')


#-------------------------------------- CITIES
@login_required
def cities_index(request):
    cities = City.objects.all()

    return render(request, 'cities/index.html', { 'cities' : cities })

@login_required
def city_detail(request, city_id):
    city = City.objects.get(id=city_id)
    return render(request, 'cities/detail.html', { 'city' : city })


#-------------------------------------- AUTHORS
@login_required
def authors_index(request):
    articles = Article.objects.filter(author=request.user)
    context = { 'articles' : articles, 'user' : request.user, 'author' : request.user.author }
    return render(request, 'authors/index.html', context)

@login_required
def author_detail(request, author_id):
    author = Author.objects.get(id=author_id)
    return render(request, 'authors/detail.html', { author : author })


#-------------------------------------- ARTICLES

def articles_index(request):
    """Show all articles."""
    articles = Article.objects.order_by('created_on')
    context = {'articles': articles}
    return render(request, 'articles/index.html', context)

def article_detail(request, article_id):
    """Show a single article."""
    article = Article.objects.get(id=article_id)
    context = {'article': article}
    return render(request, 'articles/detail.html', context)
