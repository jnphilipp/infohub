from django.db import models
from feeds.models import Feed
from south.modelsinspector import add_introspection_rules
add_introspection_rules([], ["^bundestag\.models\.TextFieldSingleLine"])

class TextFieldSingleLine(models.TextField):
	pass

class Plenarprotokoll(Feed):
	class Meta:
		verbose_name_plural = 'Plenarprotokolle'