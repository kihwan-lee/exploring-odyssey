from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django.db.models.signals import post_save
from django.dispatch import receiver

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

    joined_on = models.DateTimeField(auto_now_add=True)

    imageURL = models.ImageField(upload_to = 'profile_image', blank=True, default = '', null = True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null = True)
    
    def __str__(self):
        return self.name

    def get_full_name(self):
        return f'{self.user.firstname} {self.user.lastname}'
    
    def get_posts(self):
        return self.user.posts.all()



class Article(models.Model):
    """An Article the user is writing."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_on = models.DateField(auto_now_add=True)

    author = models.ForeignKey(User, on_delete=models.CASCADE)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


#-------------------------Profile Create/Update

@receiver(post_save, sender=User)
def create_author_profile(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)
    
@receiver(post_save, sender=User)
def save_author_profile(sender, instance, **kwargs):
    instance.author.save()
