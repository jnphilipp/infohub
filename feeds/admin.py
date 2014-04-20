from django.contrib import admin
from django.db.models import Count
from django.forms import TextInput
from django.db import models
from feeds.models import Document, Feed, Parser, Report, TextFieldSingleLine
from suit.widgets import AutosizedTextarea

class DocumentAdmin(admin.ModelAdmin):
	def show_link(self, obj):
		return '<a href="%s"><i class="icon-eye-open icon-alpha75"></i>View on site</a>' % obj.get_absolute_url()

	list_display = ('url', 'title', 'updated_at', 'feed', 'show_link')
	list_filter = ('feed', 'state')
	readonly_fields = ('slug', 'state')
	search_fields = ('slug', 'url', 'title', 'feed__title')
	ordering = ('-updated_at', 'feed')
	show_link.allow_tags = True
	show_link.short_description = 'View on site'

	formfield_overrides = {
		TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
		models.TextField: {'widget': AutosizedTextarea(attrs={'rows': 10, 'class': 'span12'})},
	}

	fieldsets = [
		(None, {'fields': ['slug', 'state', 'url', 'title', 'meta', 'content', 'text']}),
	]

class FeedAdmin(admin.ModelAdmin):
	def show_link(self, obj):
		return '<a href="%s"><i class="icon-eye-open icon-alpha75"></i>View on site</a>' % obj.get_absolute_url()

	def queryset(self, request):
		return Feed.objects.annotate(document_count=Count('document'))

	def show_document_count(self, inst):
		return inst.document_count

	list_display = ('url', 'title', 'updated_at', 'show_document_count', 'show_link')
	list_filter = ('alive', 'parser')
	readonly_fields = ('slug',)
	search_fields = ('url', 'title')
	ordering = ('-updated_at', 'url','title')
	show_document_count.admin_order_field = 'document_count'
	show_document_count.short_description = 'Number of Documents'
	show_link.allow_tags = True
	show_link.short_description = 'View on site'

	formfield_overrides = {
		TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
	}

	fieldsets = [
		(None, {'fields': ['slug', 'url', 'title', 'alive', 'parser']}),
	]

class ReportAdmin(admin.ModelAdmin):
	def show_link(self, obj):
		return '<a href="%s"><i class="icon-eye-open icon-alpha75"></i>View on site</a>' % obj.get_absolute_url()

	list_display = ('created_at', 'show_link')
	list_filter = ('created_at',)
	readonly_fields = ('slug',)
	ordering = ('-created_at',)
	show_link.allow_tags = True
	show_link.short_description = 'View on site'

	fieldsets = [
		(None, {'fields': ['slug', 'text']}),
	]

class ParserAdmin(admin.ModelAdmin):
	list_display = ('name',)
	list_filter = ()
	readonly_fields = ('slug',)
	search_fields = ('name',)
	ordering = ('name',)

	formfield_overrides = {
		TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
	}

	fieldsets = [
		(None, {'fields': ['slug', 'name']}),
	]

admin.site.register(Document, DocumentAdmin)
admin.site.register(Feed, FeedAdmin)
admin.site.register(Report, ReportAdmin)
admin.site.register(Parser, ParserAdmin)