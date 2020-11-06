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

# class Location(models.Model):
#     region_id = models.IntegerField(default = '', null=True)
#     region_name = models.CharField(max_length=100)
#     location = models.IntegerField(default = '', null=True)
#     location_desc = models.CharField(max_length=1000)
#     english_proficiency = models.BooleanField(default = '', null=True)
#     primary_lang = models.CharField(max_length=50)
#     currency = models.CharField(max_length= 20)
#     ideal_season = models.CharField(max_length=20)
#     poi_1 = models.CharField(max_length = 500)
#     poi_2 = models.CharField(max_length = 500)
#     poi_3 = models.CharField(max_length = 500)
#     url = models.URLField(max_length=250, blank= True)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     city = models.ForeignKey(City, on_delete=models.CASCADE, null = True)
    
#     class Meta:
#         verbose_name_plural='locations'
#         managed = False
#         db_table = "location"

        
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
    # location = models.ForeignKey(Location, on_delete=models.CASCADE, null=True)
    
    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateField(auto_now_add=True)
    active = models.BooleanField(default=True)

    article = models.ForeignKey(Article, on_delete=models.CASCADE, related_name="comments")

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)


#-------------------------Profile Create/Update

@receiver(post_save, sender=User)
def create_author_profile(sender, instance, created, **kwargs):
    if created:
        Author.objects.create(user=instance)
    
@receiver(post_save, sender=User)
def save_author_profile(sender, instance, **kwargs):
    instance.author.save()
