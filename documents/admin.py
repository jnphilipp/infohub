from django.contrib import admin
from django.forms import TextInput
from django.db import models
from documents.models import Document, TextFieldSingleLine
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
		(None, {'fields': ['slug', 'state', 'url', 'title', 'feed', 'meta', 'content', 'text']}),
	]

admin.site.register(Document, DocumentAdmin)