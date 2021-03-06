from django.urls import path, include
from . import views
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    # Static Routes
    path('', views.home, name='home'),

    # Location Routes
    path('locations/', views.location_index, name='location_index'),
    path('locations/<int:location_id>', views.location_detail, name='location_detail'),

    # Article Routes
    # Page that shows all articles.
    path('articles/', views.articles_index, name='articles_index'),
    
    # Detail page for a single article.
    path('articles/<int:article_id>/', views.article_detail, name='article_detail'),
    path('articles/<int:article_id>/edit/', views.edit_article, name='edit_article'),
    path('articles/<int:article_id>/delete/', views.delete_article, name='delete_article'),
    path('locations/<int:location_id>/articles/add/', views.article_add, name='article_add'),

    # Author Routes
    path('authors/', views.authors_index, name='authors_index'),
    path('authors/<int:user_id>/edit/', views.author_edit, name='author_edit'),
    # path('authors/<int:user_id>', views.author_detail, name='author_detail'),

    # Comments Routes
    # Page for editing a comment
    path('comments/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('comments/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

    
    #Auth
    path('registration/signup/', views.signup, name='signup'),

    # Login Re-direct Route
    path('', views.login, name='loginError')
]

