from django.urls import path, include
from . import views 
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    # Static Routes
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),

    # City Routes
    path('cities/', views.cities_index, name='cities_index'),
    # path('cities/new/', views.add_city, name='add_city'),
    # path('cities/<int:city_id>/delete', views.delete_city, name='delete_city),
    path('cities/<int:city_id>', views.city_detail, name='city_detail'),
    # path('cities/<int:city)/edit/' views.edit_city, name='edit_city'),

    # Article Routes
    # Page that shows all articles.
    path('articles/', views.articles_index, name='articles_index'),
    # Detail page for a single article.
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),

    # path('cities/<int:city_id>/add_article/', views.add_article, name='add_article'),

    # Author Routes
    path('authors/', views.authors_index, name='authors_index'),
    # path('authors/<int:user_id>', views.author_detail, name='author_detail'),

    #Auth
    path('registration/signup/', views.signup, name='signup')
]

