from django.contrib import admin
from django.db.models import Count
from django.forms import TextInput
from django.db import models
from feeds.models import Feed, TextFieldSingleLine

class FeedAdmin(admin.ModelAdmin):
	#def show_link(self, obj):
	#	return '<a href="%s"><i class="icon-eye-open icon-alpha75"></i>View on site</a>' % obj.get_absolute_url()

	def queryset(self, request):
		return Feed.objects.annotate(document_count=Count('document'))

	def show_document_count(self, inst):
		return inst.document_count

	list_display = ('url', 'title', 'show_document_count')
	readonly_fields = ('slug',)
	search_fields = ('url', 'title')
	ordering = ('url','title')
	show_document_count.admin_order_field = 'document_count'
	show_document_count.short_description = 'Number of Documents'
	#show_link.allow_tags = True
	#show_link.short_description = 'View on site'

	formfield_overrides = {
		models.TextField: {'widget': TextInput(attrs={'autocomplete':'off'})},
	}

	fieldsets = [
		(None, {'fields': ['slug', 'url', 'title', 'update_time', 'alive']}),
	]

admin.site.register(Feed, FeedAdmin)