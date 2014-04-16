from datetime import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from south.modelsinspector import add_introspection_rules

import feedparser

add_introspection_rules([], ["^feeds\.models\.TextFieldSingleLine"])

def tag_content(tag, content):
	return '<%s>%s</%s>' % (tag, content, tag)

class TextFieldSingleLine(models.TextField):
	pass

class Feed(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	slug = models.SlugField(max_length=4096, unique=True)
	url = TextFieldSingleLine(unique=True)
	title = TextFieldSingleLine(blank=True, null=True)
	alive = models.BooleanField(default=True)

	def get_absolute_url(self):
		return reverse('feed', args=[str(self.slug)])

	def parse(self):
		rssfeed = feedparser.parse(self.url)
		for entry in rssfeed.entries:
			if not Document.objects.filter(url=entry.link).filter(feed=self).exists():
				url = entry.link
				title = entry.title.replace('\n', '')
				summary = entry.summary if 'summary' in entry else ''

				date = None
				if 'published' in entry:
					date = entry.published_parsed
				elif 'updated' in entry:
					date = entry.updated_parsed
				elif 'created' in entry:
					date = entry.created_parsed

				meta = tag_content('title', title)
				if date:
					meta += tag_content('date', datetime(*date[:6]).isoformat())

				Document.objects.create(url=url, feed=self, content=summary, meta=meta)

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
	meta = models.TextField()
	content = models.TextField()
	feed = models.ForeignKey(Feed)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.url)
		super(Document, self).save(*args, **kwargs)

	def __str__(self):
		return self.url

	class Meta:
		ordering = ('updated_at',)