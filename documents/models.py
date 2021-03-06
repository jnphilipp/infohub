from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django_fsm import FSMField, transition
from feeds.models import Feed
from importlib import import_module
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^documents\.models\.TextFieldSingleLine"])

class TextFieldSingleLine(models.TextField):
	pass

class Document(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	slug = models.SlugField(max_length=4096, unique=True)
	url = TextFieldSingleLine(unique=True)
	title = TextFieldSingleLine(null=True, blank=True)
	meta = models.TextField()
	content = models.TextField()
	text = models.TextField(null=True, blank=True)
	feed = models.ForeignKey(Feed)

	state = FSMField(default='new', protected=True)

	@transition(field=state, source='new', target='parsed')
	def parse(self):
		if not self.feed.parser:
			raise Exception('No parser defined.')

		module = import_module('parsers.parsers')
		c = getattr(module, self.feed.parser.slug)
		parser = c()
		parser.get_text(self)

		if not self.text:
			raise Exception('Could not parse text.')

	def get_absolute_url(self):
		return reverse('document', args=[str(self.slug)])

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.url)
		super(Document, self).save(*args, **kwargs)

	def __str__(self):
		return self.title if self.title else self.url

	class Meta:
		ordering = ('-created_at',)