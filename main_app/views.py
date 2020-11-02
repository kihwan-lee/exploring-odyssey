from main_app.forms import Article_Form
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import City, Author, Article
#from .forms import

#---------------------ADMIN---------------------------

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
    
    user_form=UserCreationForm()
    context = {'user form': user_form, 'error_message': error_message}
    return render(request, 'accounts/signup.html', context)


def home (request):
    return render(request, 'home.html')

#----------------------Cities---------------------------

def cities_index(request):
    cities = City.objects.all()
    return render(request, 'cities/index.html', { 'cities' : cities })

def city_detail(request, city_id):
    city = City.objects.get(id=city_id)
    return render(request, 'cities/detail.html', { 'city' : city })

#----------------------Authors-------------------------------

def authors_index(request):
    authors = Author.objects.all()
    return render(request, 'authors/index.html', { 'authors' : authors })

def author_detail(request, author_id):
    author = Author.objects.get(id=author_id)
    return render(request, 'authors/detail.html', { author : author })

