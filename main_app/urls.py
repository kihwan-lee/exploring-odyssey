from django.urls import path, include
from . import views 
from django.conf.urls.static import static
from .models import City, Author, Article

urlpatterns = [ 
    path('', views.home, name='home'),
    path('accounts/signup/', views.signup, name='signup'),
    path('cities/', views.cities_index, name='cities_index'),
    path('authors/', views.authors_index, name='authors_index'),
    path('cities/<int:city_id>', views.city_detail, name='city_detail'),
    path('authors/<int:author_id>', views.author_detail, name='author_detail')
]

