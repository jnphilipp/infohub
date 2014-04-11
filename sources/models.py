from datetime import datetime
from django.core.urlresolvers import reverse
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.generic import GenericForeignKey,GenericRelation
from django.db import models
from django.template.defaultfilters import slugify
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^sources\.models\.TextFieldSingleLine"])

class TextFieldSingleLine(models.TextField):
	pass

class Source(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	slug = models.SlugField(max_length=4096, unique=True)
	url = TextFieldSingleLine(unique=True)
	title = TextFieldSingleLine(blank=True, null=True)
	update_time = models.DateTimeField(default=datetime.now)
	alive = models.BooleanField(default=True)
	documents = GenericRelation('Document')

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.url)
		super(Source, self).save(*args, **kwargs)

	def __str__(self):
		return self.title if self.title else self.url

	class Meta:
		abstract = True

class Document(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	slug = models.SlugField(max_length=4096, unique=True)
	url = TextFieldSingleLine(unique=True)
	meta = models.TextField()
	content = models.TextField()
	content_type = models.ForeignKey(ContentType)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey()

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.url)
		super(Document, self).save(*args, **kwargs)

	def __str__(self):
		return self.url