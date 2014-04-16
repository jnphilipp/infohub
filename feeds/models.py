from django.db import models
from south.modelsinspector import add_introspection_rules
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

	def parse(self):
		pass

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