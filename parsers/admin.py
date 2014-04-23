from django.contrib import admin
from django.db.models import Count
from django.forms import TextInput
from parsers.models import Parser, TextFieldSingleLine

class ParserAdmin(admin.ModelAdmin):
	def queryset(self, request):
		return Parser.objects.annotate(feed_count=Count('feed'))

	def show_feed_count(self, inst):
		return inst.feed_count

	list_display = ('name', 'slug', 'show_feed_count')
	list_filter = ('feed',)
	readonly_fields = ('slug',)
	search_fields = ('name',)
	ordering = ('name',)
	show_feed_count.admin_order_field = 'feed_count'
	show_feed_count.short_description = 'Number of Feeds'

	formfield_overrides = {
		TextFieldSingleLine: {'widget': TextInput(attrs={'autocomplete':'off'})},
	}

	fieldsets = [
		(None, {'fields': ['slug', 'name']}),
	]

admin.site.register(Parser, ParserAdmin)