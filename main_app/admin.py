from django.contrib import admin
from .models import * 

# Register your models here.
admin.site.register(Article)
admin.site.register(Author)
admin.site.register(Comment)
admin.site.register(Location)

class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'body', 'article', 'created_on', 'active')
	list_filter = ('active', 'created_on')
	search_fields = ('name', 'email', 'body')
	actions = ['approve_comments']

	def approve_comments(self, request, queryset):
		queryset.update(active=True)

class LocationAdmin(admin.ModelAdmin):
	list_display = (
		'region_name', 
		'location_name', 
		'location_desc', 
		'english_proficiency', 
		'primary_lang',
		'currency',
		'ideal_season',
		'poi_1',
		'poi_2',
		'poi_3')
	# list_filter = ('active', 'created_on')
	search_fields = (
		'region_name', 
		'location_name', 
		'location_desc', 
		'english_proficiency', 
		'primary_lang',
		'currency',
		'ideal_season',
		'poi_1',
		'poi_2',
		'poi_3')
	# actions = ['approve_comments']

	# def approve_comments(self, request, queryset):
	# 	queryset.update(active=True)