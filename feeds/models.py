from datetime import datetime
from django.core.urlresolvers import reverse
from django.db import models
from django.template.defaultfilters import slugify
from parsers.models import Parser
from south.modelsinspector import add_introspection_rules

import feedparser
import re

add_introspection_rules([], ["^feeds\.models\.TextFieldSingleLine"])

class TextFieldSingleLine(models.TextField):
	pass

class Feed(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	slug = models.SlugField(max_length=4096, unique=True)
	url = TextFieldSingleLine(unique=True)
	title = TextFieldSingleLine(blank=True, null=True)
	alive = models.BooleanField(default=True)

	parser = models.ForeignKey(Parser, null=True, blank=True)

	def get_absolute_url(self):
		return reverse('feed', args=[str(self.slug)])

	def parse(self):
		from documents.models import Document
		rssfeed = feedparser.parse(self.url)
		if not self.title and rssfeed.feed.title:
			self.title = rssfeed.feed.title
			self.save()

		for entry in rssfeed.entries:
			if not Document.objects.filter(url=entry.link).exists():
				title = re.sub(r'\s\s+', ' ', entry.title.replace('\n', ' '))
				summary = re.sub(r'\s\s+', ' ', entry.summary.replace('\n', ' ')) if 'summary' in entry else ''

				date = None
				if 'published' in entry:
					date = entry.published_parsed
				elif 'updated' in entry:
					date = entry.updated_parsed
				elif 'created' in entry:
					date = entry.created_parsed

				meta = ''
				if date:
					meta += '<date>%s</date>' % datetime(*date[:6]).isoformat()

				Document.objects.create(url=entry.link, title=title, feed=self, content=summary, meta=meta)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.url)
		super(Feed, self).save(*args, **kwargs)

	def __str__(self):
		return self.title if self.title else self.url

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