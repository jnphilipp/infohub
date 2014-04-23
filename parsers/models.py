from django.db import models
from django.template.defaultfilters import slugify
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^parsers\.models\.TextFieldSingleLine"])

class TextFieldSingleLine(models.TextField):
	pass

class Parser(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	slug = models.SlugField(max_length=4096, unique=True)
	name = TextFieldSingleLine(unique=True)

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.name).replace('-', '_')
		super(Parser, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

	class Meta:
		ordering = ('name',)