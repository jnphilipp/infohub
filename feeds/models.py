from datetime import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from django_fsm import FSMField, transition
from south.modelsinspector import add_introspection_rules

import feedparser
import re

add_introspection_rules([], ["^feeds\.models\.TextFieldSingleLine"])

def tag_content(tag, content):
	return '<%s>%s</%s>' % (tag, content, tag)

class TextFieldSingleLine(models.TextField):
	pass

class Parser(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	slug = models.SlugField(max_length=4096, unique=True)
	name = TextFieldSingleLine(unique=True)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name)
		super(Parser, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ('name',)

class Feed(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	slug = models.SlugField(max_length=4096, unique=True)
	url = TextFieldSingleLine(unique=True)
	title = TextFieldSingleLine(blank=True, null=True)
	alive = models.BooleanField(default=True)

	parser = models.ForeignKey(Parser, default=Parser.objects.get(slug='default'))

	def get_absolute_url(self):
		return reverse('feed', args=[str(self.slug)])

	def parse(self):
		rssfeed = feedparser.parse(self.url)
		if not self.title and rssfeed.feed.title:
			self.title = rssfeed.feed.title
			self.save()

		for entry in rssfeed.entries:
			if not Document.objects.filter(url=entry.link).exists():
				title = re.sub(r'\s\s+', ' ', entry.title.replace('\n', ''))
				summary = entry.summary if 'summary' in entry else ''

				date = None
				if 'published' in entry:
					date = entry.published_parsed
				elif 'updated' in entry:
					date = entry.updated_parsed
				elif 'created' in entry:
					date = entry.created_parsed

				meta = ''
				if date:
					meta += tag_content('date', datetime(*date[:6]).isoformat())

				Document.objects.create(url=entry.link, title=title, feed=self, content=summary, meta=meta)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.url)
		super(Feed, self).save(*args, **kwargs)

	def __str__(self):
		return self.title if self.title else self.url

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

	@transition(field=state, source='new', target='text')
	def parse_text(self):
		pass

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

class Report(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	slug = models.SlugField(max_length=4096, unique=True)
	text = models.TextField()

	def get_absolute_url(self):
		return reverse('report', args=[str(self.slug)])

	def save(self, *args, **kwargs):
		super(Report, self).save(*args, **kwargs)
		if not self.slug:
			self.slug = slugify(self.created_at.isoformat())
			super(Report, self).save()

	def __str__(self):
		return self.slug

	class Meta:
		ordering = ('-created_at',)