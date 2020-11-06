from django.contrib import admin
from .models import * 

# Register your models here.
admin.site.register(City)
admin.site.register(Article)
admin.site.register(Author)
admin.site.register(Comment)

class CommentAdmin(admin.ModelAdmin):
	list_display = ('name', 'body', 'article', 'created_on', 'active')
	list_filter = ('active', 'created_on')
	search_fields = ('name', 'email', 'body')
	actions = ['approve_comments']

	def approve_comments(self, request, queryset):
		queryset.update(active=True)