from django.urls import path, include
from . import views 
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    # Static Routes
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # Cities Routes
    path('cities/', views.cities_index, name='cities_index'),
    # path('cities/new/', views.add_city, name='add_city'),
    # path('cities/<int:city_id>/delete', views.delete_city, name='delete_city),
    path('cities/<int:city_id>', views.city_detail, name='city_detail'),
    # path('cities/<int:city)/edit/' views.edit_city, name='edit_city'),

    # Articles Routes
    # Page that shows all articles.
    path('articles/', views.articles, name='articles'),
    
    # path('cities/<int:city_id>/add_article/', views.add_article, name='add_article'),

    # Authors Routes
    path('authors/', views.authors_index, name='authors_index'),
    path('authors/<int:author_id>', views.author_detail, name='author_detail'),

    #Auth
    path('accounts/signup/', views.signup, name='signup')
]

