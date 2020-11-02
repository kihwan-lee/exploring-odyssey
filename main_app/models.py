from django.db import models
from django.contrib.auth.models import User
from datetime import date

# Create your models here.

class City(models.Model):
    #handle city/state separately?
    name = models.CharField(max_length=100)
    image = models.CharField(max_length=250, default = '')
    
    class Meta:
        verbose_name_plural='cities'

    def __str__(self):
        return self.name

        
class Author(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    joined_on = models.DateField(auto_now_add=True)
    imageURL = models.ImageField(upload_to = 'profile_image', blank=True, default = '')
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

    def get_full_name(self):
        return f'{self.user.firstname} {self.user.lastname}'
    
    def get_posts(self):
        return self.user.posts.all()


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created_on = models.DateField(auto_now_add=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
